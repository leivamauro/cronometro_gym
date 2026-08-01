import React from 'react';
import { FontOption } from '../types';
import { Volume2, VolumeX, Maximize, RefreshCw, Type, List } from 'lucide-react';

interface ExtraSettingsProps {
  fontStyle: FontOption;
  setFontStyle: (font: FontOption) => void;
  soundEnabled: boolean;
  setSoundEnabled: (enabled: boolean) => void;
  onAddLap?: () => void;
  showLaps: boolean;
  setShowLaps: (show: boolean) => void;
  onResetApp: () => void;
}

export const ExtraSettings: React.FC<ExtraSettingsProps> = ({
  fontStyle,
  setFontStyle,
  soundEnabled,
  setSoundEnabled,
  onAddLap,
  showLaps,
  setShowLaps,
  onResetApp,
}) => {
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
      }
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 mt-6 pt-4 border-t border-gray-800/80 flex flex-wrap items-center justify-between gap-3 text-xs text-gray-400 select-none">
      {/* Font selector */}
      <div className="flex items-center gap-1.5 bg-[#1a1f26] px-3 py-1.5 rounded-lg border border-gray-800">
        <Type size={14} className="text-gray-400" />
        <span className="text-[11px] text-gray-400 mr-1 hidden sm:inline">Fuente:</span>
        <button
          onClick={() => setFontStyle('handwritten')}
          className={`px-2 py-0.5 rounded text-[11px] transition-colors ${
            fontStyle === 'handwritten'
              ? 'bg-[#3b434f] text-white font-bold'
              : 'hover:text-gray-200'
          }`}
        >
          Architects
        </button>
        <button
          onClick={() => setFontStyle('caveat')}
          className={`px-2 py-0.5 rounded text-[11px] transition-colors ${
            fontStyle === 'caveat' ? 'bg-[#3b434f] text-white font-bold' : 'hover:text-gray-200'
          }`}
        >
          Caveat
        </button>
        <button
          onClick={() => setFontStyle('comic')}
          className={`px-2 py-0.5 rounded text-[11px] transition-colors ${
            fontStyle === 'comic' ? 'bg-[#3b434f] text-white font-bold' : 'hover:text-gray-200'
          }`}
        >
          Comic
        </button>
      </div>

      {/* Control Action Tools */}
      <div className="flex items-center gap-2">
        {onAddLap && (
          <button
            onClick={() => setShowLaps(!showLaps)}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-[11px] transition-all cursor-pointer ${
              showLaps
                ? 'bg-gray-800 border-gray-600 text-white'
                : 'bg-[#1a1f26] border-gray-800 text-gray-400 hover:text-white'
            }`}
            title="Ver/ocultar historial de vueltas"
          >
            <List size={14} />
            <span>Vueltas</span>
          </button>
        )}

        <button
          onClick={() => setSoundEnabled(!soundEnabled)}
          className="p-1.5 rounded-lg bg-[#1a1f26] border border-gray-800 text-gray-400 hover:text-white transition-colors cursor-pointer"
          title={soundEnabled ? 'Sonido activado' : 'Sonido desactivado'}
        >
          {soundEnabled ? <Volume2 size={14} /> : <VolumeX size={14} />}
        </button>

        <button
          onClick={toggleFullscreen}
          className="p-1.5 rounded-lg bg-[#1a1f26] border border-gray-800 text-gray-400 hover:text-white transition-colors cursor-pointer"
          title="Pantalla completa"
        >
          <Maximize size={14} />
        </button>
      </div>
    </div>
  );
};
