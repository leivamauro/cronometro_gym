import React from 'react';
import { StopwatchStatus, FontOption } from '../types';

interface ControlButtonsProps {
  status: StopwatchStatus;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
  fontStyle: FontOption;
}

export const ControlButtons: React.FC<ControlButtonsProps> = ({
  status,
  onStart,
  onPause,
  onReset,
  fontStyle,
}) => {
  const fontClass =
    fontStyle === 'handwritten'
      ? 'font-handwritten'
      : fontStyle === 'caveat'
      ? 'font-casual'
      : 'font-comic';

  return (
    <div className="w-full max-w-2xl mx-auto px-2 mt-6 mb-4">
      <div className="flex items-center justify-center gap-4 sm:gap-6">
        {/* Iniciar Button */}
        <button
          onClick={onStart}
          disabled={status === 'running'}
          className={`flex-1 min-w-[120px] sm:min-w-[180px] py-3.5 sm:py-4 px-6 bg-[#3a3a3c] hover:bg-[#48484a] active:scale-95 text-white font-bold text-xl sm:text-2xl md:text-3xl rounded-2xl transition-all shadow-[0_4px_15px_rgba(0,0,0,0.4)] border border-white/5 select-none cursor-pointer ${
            status === 'running' ? 'opacity-50 ring-2 ring-emerald-500/50' : 'hover:shadow-lg'
          }`}
        >
          <span className={fontClass}>Iniciar</span>
        </button>

        {/* Pausar Button */}
        <button
          onClick={onPause}
          disabled={status !== 'running'}
          className={`flex-1 min-w-[120px] sm:min-w-[180px] py-3.5 sm:py-4 px-6 bg-[#3a3a3c] hover:bg-[#48484a] active:scale-95 text-white font-bold text-xl sm:text-2xl md:text-3xl rounded-2xl transition-all shadow-[0_4px_15px_rgba(0,0,0,0.4)] border border-white/5 select-none cursor-pointer ${
            status !== 'running' ? 'opacity-40 cursor-not-allowed' : 'hover:shadow-lg'
          }`}
        >
          <span className={fontClass}>Pausar</span>
        </button>

        {/* Reiniciar Button */}
        <button
          onClick={onReset}
          className="flex-1 min-w-[120px] sm:min-w-[180px] py-3.5 sm:py-4 px-6 bg-[#3a3a3c] hover:bg-[#48484a] active:scale-95 text-white font-bold text-xl sm:text-2xl md:text-3xl rounded-2xl transition-all shadow-[0_4px_15px_rgba(0,0,0,0.4)] border border-white/5 select-none cursor-pointer hover:shadow-lg"
        >
          <span className={fontClass}>Reiniciar</span>
        </button>
      </div>
    </div>
  );
};
