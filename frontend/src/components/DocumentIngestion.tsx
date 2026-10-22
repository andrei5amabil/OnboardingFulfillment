import React, { useState } from 'react';
import { FileSignature, CreditCard, HeartPulse, Layers, AlertTriangle } from 'lucide-react';
import { DocumentDropzone } from './DocumentDropzone';
import type { DocumentType, ExtractionResponse } from '../types/extraction';
import { fetchWithAuth } from '../lib/api';

interface DocumentIngestionProps {
  apiBaseUrl: string;
  onboardingRunId: string;
  onExtractionSuccess: (docType: DocumentType, payload: ExtractionResponse) => void;
}

export const DocumentIngestion: React.FC<DocumentIngestionProps> = ({
  apiBaseUrl,
  onboardingRunId,
  onExtractionSuccess,
}) => {
  const [files, setFiles] = useState<Record<DocumentType, File | null>>({
    contract: null,
    national_id: null,
    medical_clearance: null,
  });

  const [scanningMap, setScanningMap] = useState<Record<DocumentType, boolean>>({
    contract: false,
    national_id: false,
    medical_clearance: false,
  });

  const [successMap, setSuccessMap] = useState<Record<DocumentType, boolean>>({
    contract: false,
    national_id: false,
    medical_clearance: false,
  });

  const [alerts, setAlerts] = useState<string[]>([]);
  const isAnyScanning = Object.values(scanningMap).some(Boolean);

  const handleFileChange = (docType: DocumentType, file: File | null) => {
    setFiles((prev) => ({ ...prev, [docType]: file }));
    if (!file) {
      setSuccessMap((prev) => ({ ...prev, [docType]: false }));
    }
  };

  const uploadAndExtract = async (docType: DocumentType, file: File): Promise<boolean> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', docType);
    formData.append('onboarding_run_id', onboardingRunId);

    setScanningMap((prev) => ({ ...prev, [docType]: true }));

    try {
      const response = await fetchWithAuth(`${apiBaseUrl}/onboarding/extract-document`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      const result: ExtractionResponse = await response.json();

      setSuccessMap((prev) => ({ ...prev, [docType]: true }));
      if (result.confidence_flags?.length) {
        setAlerts((prev) => [...prev, ...result.confidence_flags]);
      }

      onExtractionSuccess(docType, result);
      return true;
    } catch (err: any) {
      alert(`Failed to extract ${file.name}: ${err.message}`);
      return false;
    } finally {
      setScanningMap((prev) => ({ ...prev, [docType]: false }));
    }
  };

  const scanBatch = async (typesToScan: DocumentType[]) => {
    setAlerts([]);
    for (const docType of typesToScan) {
      const file = files[docType];
      if (file) {
        await uploadAndExtract(docType, file);
      }
    }
  };

  const activeFilesCount = Object.values(files).filter(Boolean).length;

  return (
    <div className="space-y-4">
      <div className="border-b border-slate-300 pb-3">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-900">
          1. Document Upload & Extraction
        </h2>
        <p className="text-xs text-slate-700 mt-0.5">
          Attach identity, contract, and medical documents to populate candidate records automatically.
        </p>
      </div>

      {alerts.length > 0 && (
        <div className="p-3 bg-amber-50 border border-amber-300 rounded-xl space-y-1">
          {alerts.map((alert, idx) => (
            <div key={idx} className="flex items-center gap-2 text-xs font-semibold text-amber-950">
              <AlertTriangle className="w-4 h-4 shrink-0 text-amber-700" />
              <span>{alert}</span>
            </div>
          ))}
        </div>
      )}

      {/* 3-Column Dropzone Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DocumentDropzone
          docType="contract"
          title="Employment Contract"
          description="Role, manager, dates & address"
          icon={FileSignature}
          file={files.contract}
          onFileSelect={(file) => handleFileChange('contract', file)}
          onScanSingle={() => files.contract && uploadAndExtract('contract', files.contract)}
          isScanning={scanningMap.contract}
          isSuccess={successMap.contract}
          disabled={isAnyScanning}
        />

        <DocumentDropzone
          docType="national_id"
          title="National ID Card"
          description="Legal full name & CNP"
          icon={CreditCard}
          file={files.national_id}
          onFileSelect={(file) => handleFileChange('national_id', file)}
          onScanSingle={() => files.national_id && uploadAndExtract('national_id', files.national_id)}
          isScanning={scanningMap.national_id}
          isSuccess={successMap.national_id}
          disabled={isAnyScanning}
        />

        <DocumentDropzone
          docType="medical_clearance"
          title="Medical Clearance"
          description="Fitness verification & examination date"
          icon={HeartPulse}
          file={files.medical_clearance}
          onFileSelect={(file) => handleFileChange('medical_clearance', file)}
          onScanSingle={() => files.medical_clearance && uploadAndExtract('medical_clearance', files.medical_clearance)}
          isScanning={scanningMap.medical_clearance}
          isSuccess={successMap.medical_clearance}
          disabled={isAnyScanning}
        />

        <button
          type="button"
          onClick={() => {
            const queue = (Object.keys(files) as DocumentType[]).filter((key) => files[key]);
            scanBatch(queue);
          }}
          disabled={activeFilesCount === 0 || isAnyScanning}
          className="col-span-1 md:col-span-3 w-full flex items-center justify-center gap-2 py-3 px-4 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
        >
          <Layers className="w-4 h-4 text-white" />
          <span>Extract All Uploaded Files ({activeFilesCount} Ready)</span>
        </button>
      </div>
    </div>
  );
};