import React from 'react';
import { X, FileText } from 'lucide-react';
import { DocumentUpload } from './DocumentUpload';
import { DocumentList } from './DocumentList';
import { cn } from '../../utils/cn';

interface DocumentPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DocumentPanel: React.FC<DocumentPanelProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = React.useState<'upload' | 'list'>('upload');

  if (!isOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="fixed right-0 top-0 bottom-0 w-full md:w-[500px] bg-white shadow-xl z-50 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <FileText size={20} className="text-primary-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Document Management
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('upload')}
            className={cn(
              'flex-1 px-4 py-3 font-medium text-sm transition-colors',
              activeTab === 'upload'
                ? 'border-b-2 border-primary-600 text-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            )}
          >
            Upload
          </button>
          <button
            onClick={() => setActiveTab('list')}
            className={cn(
              'flex-1 px-4 py-3 font-medium text-sm transition-colors',
              activeTab === 'list'
                ? 'border-b-2 border-primary-600 text-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            )}
          >
            Documents
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === 'upload' ? <DocumentUpload /> : <DocumentList />}
        </div>
      </div>
    </>
  );
};
