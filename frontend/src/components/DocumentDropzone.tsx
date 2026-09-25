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
const MAX_FILE_SIZE = 15 * 1024 * 1024; // 15MB limit matching preprocessing.py

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
    <div className="flex flex-col h-full rounded-xl border border-slate-700 bg-slate-800/60 p-4 transition-colors">
      <div className="flex items-center gap-2 mb-3">
        <div className="p-2 rounded-lg bg-slate-700/50 text-indigo-400">
          <Icon className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-slate-100">{title}</h3>
          <p className="text-xs text-slate-400">{description}</p>
        </div>
      </div>

      {/* Native Drag & Drop Target */}
      <div
        onClick={() => !disabled && !isScanning && inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled && !isScanning) setIsDragActive(true);
        }}
        onDragLeave={() => setIsDragActive(false)}
        onDrop={handleDrop}
        className={`flex-1 flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-5 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-500/10'
            : isSuccess
            ? 'border-emerald-500/40 bg-emerald-500/5'
            : 'border-slate-600 hover:border-slate-500 bg-slate-900/40'
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
          <div className="flex flex-col items-center gap-2 text-slate-300">
            <FileText className="w-8 h-8 text-indigo-400" />
            <div className="max-w-[200px] truncate text-xs font-medium text-slate-200" title={file.name}>
              {file.name}
            </div>
            <span className="text-[10px] text-slate-400">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-1.5 text-slate-400">
            <UploadCloud className="w-7 h-7 text-slate-500 mb-1" />
            <p className="text-xs font-medium text-slate-300">
              {isDragActive ? 'Drop document here' : 'Drag & drop or browse'}
            </p>
            <p className="text-[11px] text-slate-500">PDF, PNG, JPG up to 15MB</p>
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
            className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-700/50 rounded-lg transition-colors"
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
          className="flex-1 flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {isScanning ? (
            <>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Scanning...
            </>
          ) : isSuccess ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-300" />
              Re-scan Document
            </>
          ) : (
            `Scan ${title}`
          )}
        </button>
      </div>
    </div>
  );
};