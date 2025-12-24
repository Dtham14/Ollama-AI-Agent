import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { useDocumentStore } from '../../stores/documentStore';
import { cn } from '../../utils/cn';

export const DocumentUpload: React.FC = () => {
  const [files, setFiles] = React.useState<File[]>([]);
  const [uploading, setUploading] = React.useState<Map<string, boolean>>(new Map());
  const [uploadStatus, setUploadStatus] = React.useState<Map<string, 'success' | 'error'>>(new Map());

  const { uploadDocument } = useDocumentStore();

  const onDrop = React.useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/markdown': ['.md'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = (fileName: string) => {
    setFiles((prev) => prev.filter((f) => f.name !== fileName));
    setUploadStatus((prev) => {
      const newMap = new Map(prev);
      newMap.delete(fileName);
      return newMap;
    });
  };

  const handleUpload = async () => {
    for (const file of files) {
      try {
        setUploading((prev) => new Map(prev).set(file.name, true));

        await uploadDocument(file, 'Music Theory', '', undefined);

        setUploadStatus((prev) => new Map(prev).set(file.name, 'success'));
        setUploading((prev) => {
          const newMap = new Map(prev);
          newMap.delete(file.name);
          return newMap;
        });

        // Remove file after successful upload
        setTimeout(() => removeFile(file.name), 2000);
      } catch (error) {
        setUploadStatus((prev) => new Map(prev).set(file.name, 'error'));
        setUploading((prev) => {
          const newMap = new Map(prev);
          newMap.delete(file.name);
          return newMap;
        });
      }
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-4">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={cn(
          'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors',
          isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        )}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto mb-4 text-gray-400" size={48} />
        {isDragActive ? (
          <p className="text-primary-600 font-medium">Drop files here...</p>
        ) : (
          <>
            <p className="text-gray-700 font-medium mb-2">
              Drag & drop files here, or click to select
            </p>
            <p className="text-sm text-gray-500">
              Supports: PDF, TXT, CSV, DOCX, MD (Max 10MB)
            </p>
          </>
        )}
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="font-medium text-gray-900">
              Files to Upload ({files.length})
            </h3>
            <button
              onClick={handleUpload}
              disabled={files.every((f) => uploadStatus.has(f.name))}
              className={cn(
                'px-4 py-2 rounded-lg bg-primary-600 text-white font-medium',
                'hover:bg-primary-700 transition-colors',
                'disabled:bg-gray-300 disabled:cursor-not-allowed'
              )}
            >
              Upload All
            </button>
          </div>

          <div className="space-y-2">
            {files.map((file) => {
              const isUploading = uploading.get(file.name);
              const status = uploadStatus.get(file.name);

              return (
                <div
                  key={file.name}
                  className="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg"
                >
                  <File size={20} className="text-gray-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(file.size)}
                    </p>
                  </div>

                  {isUploading && (
                    <Loader2 size={20} className="text-primary-600 animate-spin flex-shrink-0" />
                  )}
                  {status === 'success' && (
                    <CheckCircle size={20} className="text-green-600 flex-shrink-0" />
                  )}
                  {status === 'error' && (
                    <AlertCircle size={20} className="text-red-600 flex-shrink-0" />
                  )}
                  {!isUploading && !status && (
                    <button
                      onClick={() => removeFile(file.name)}
                      className="p-1 hover:bg-gray-100 rounded transition-colors flex-shrink-0"
                    >
                      <X size={16} className="text-gray-500" />
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
