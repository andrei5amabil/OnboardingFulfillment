import React, { useRef, useState } from 'react';
import { UploadCloud, CheckCircle2, FileText, Trash2, Loader2, type LucideIcon } from 'lucide-react';
import type { DocumentType } from '../types/extraction';

interface DocumentDropzoneProps {
  docType: DocumentType;
  title: string;
  description: string;
  icon: LucideIcon;
  file: File | null;
  onFileSelect: (file: File | null) => void;
  onScanSingle: () => void;
  isScanning: boolean;
  isSuccess: boolean;
  disabled?: boolean;
}

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.webp'];
const MAX_FILE_SIZE = 15 * 1024 * 1024;

export const DocumentDropzone: React.FC<DocumentDropzoneProps> = ({
  title,
  description,
  icon: Icon,
  file,
  onFileSelect,
  onScanSingle,
  isScanning,
  isSuccess,
  disabled = false,
}) => {
  const [isDragActive, setIsDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const validateAndSet = (selected: File) => {
    const isExtensionValid = ALLOWED_EXTENSIONS.some((ext) =>
      selected.name.toLowerCase().endsWith(ext)
    );
    if (!isExtensionValid) {
      alert('Invalid file format. Allowed formats: PDF, PNG, JPG, WEBP.');
      return;
    }
    if (selected.size > MAX_FILE_SIZE) {
      alert('File exceeds maximum size limit of 15MB.');
      return;
    }
    onFileSelect(selected);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragActive(false);
    if (disabled || isScanning) return;
    if (e.dataTransfer.files?.[0]) {
      validateAndSet(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-slate-300 bg-white p-4 shadow-sm">
      <div className="flex items-center gap-3 mb-3">
        <div className="p-2 rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
          <Icon className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-slate-900">{title}</h3>
          <p className="text-xs text-slate-700">{description}</p>
        </div>
      </div>

      {/* Drag & Drop Box */}
      <div
        onClick={() => !disabled && !isScanning && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled && !isScanning) setIsDragActive(true);
        }}
        onDragLeave={() => setIsDragActive(false)}
        onDrop={handleDrop}
        className={`flex-1 min-h-[140px] flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-blue-600 bg-blue-50'
            : isSuccess
            ? 'border-emerald-500 bg-emerald-50/50'
            : 'border-slate-300 hover:border-blue-600 bg-slate-50'
        } ${disabled || isScanning ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,.webp"
          className="hidden"
          onChange={(e) => {
            if (e.target.files?.[0]) validateAndSet(e.target.files[0]);
          }}
        />

        {file ? (
          <div className="flex flex-col items-center gap-1.5 text-slate-900">
            <FileText className="w-8 h-8 text-blue-600" />
            <div className="max-w-[200px] truncate text-xs font-bold text-slate-900" title={file.name}>
              {file.name}
            </div>
            <span className="text-xs text-slate-700 font-mono font-medium">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-1 text-slate-700">
            <UploadCloud className="w-7 h-7 text-slate-600 mb-0.5" />
            <p className="text-xs font-bold text-slate-900">
              {isDragActive ? 'Drop file to upload' : 'Click or drag file here'}
            </p>
            <p className="text-xs text-slate-700">PDF, PNG, JPG up to 15MB</p>
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="mt-3 flex items-center gap-2">
        {file && !isScanning && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onFileSelect(null);
            }}
            className="p-2 text-slate-600 hover:text-rose-700 hover:bg-rose-50 border border-slate-300 rounded-lg transition-colors"
            title="Remove file"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}

        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onScanSingle();
          }}
          disabled={!file || isScanning || disabled}
          className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 text-xs font-bold rounded-lg transition-colors shadow-sm ${
            isSuccess
              ? 'bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300'
              : 'bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-40 disabled:cursor-not-allowed'
          }`}
        >
          {isScanning ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              <span>Extracting...</span>
            </>
          ) : isSuccess ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
              <span>Re-extract Data</span>
            </>
          ) : (
            `Extract Data`
          )}
        </button>
      </div>
    </div>
  );
};