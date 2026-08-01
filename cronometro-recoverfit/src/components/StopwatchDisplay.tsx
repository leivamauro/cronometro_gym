import React from 'react';
import { FontOption, TimerMode } from '../types';

interface StopwatchDisplayProps {
  hours: number;
  minutes: number;
  seconds: number;
  fontStyle: FontOption;
  onOpenModal?: () => void;
  mode?: TimerMode;
}

export const StopwatchDisplay: React.FC<StopwatchDisplayProps> = ({
  hours,
  minutes,
  seconds,
  fontStyle,
  onOpenModal,
  mode = 'stopwatch',
}) => {
  // Pad numbers with leading zero
  const pad = (num: number) => String(num).padStart(2, '0');

  // Font CSS class assignment
  const fontClass =
    fontStyle === 'handwritten'
      ? 'font-handwritten'
      : fontStyle === 'caveat'
      ? 'font-casual'
      : 'font-comic';

  const formatUnits = [
    { value: pad(hours), label: 'hr' },
    { value: pad(minutes), label: 'min' },
    { value: pad(seconds), label: 'seg' },
  ];

  return (
    <div className="w-full max-w-2xl mx-auto px-2 my-2 flex flex-col items-center">
      {/* Timer Mode Badge */}
      <div className="mb-3">
        <span
          className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase transition-colors ${
            mode === 'countdown'
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              : 'bg-zinc-800/80 text-zinc-400 border border-zinc-700/50'
          }`}
        >
          {mode === 'countdown' ? '⏱️ Modo Cuenta Regresiva' : '⏱️ Modo Cronómetro'}
        </span>
      </div>

      <div className="w-full flex items-center justify-center gap-3 sm:gap-6 md:gap-8">
        {formatUnits.map((unit, index) => (
          <div key={index} className="relative flex-1 max-w-[220px] aspect-square">
            {/* Square Box with #1c1c1e Background, Inset & Drop Shadow */}
            <button
              type="button"
              onClick={onOpenModal}
              title="Haz clic para ajustar el tiempo"
              className="w-full h-full bg-[#1c1c1e] hover:bg-[#28282c] hover:border-gray-600 transition-all rounded-2xl sm:rounded-3xl border border-white/10 flex items-center justify-center relative overflow-hidden cursor-pointer group active:scale-98"
              style={{
                boxShadow:
                  'inset 0 2px 10px rgba(255,255,255,0.05), 0 10px 30px rgba(0,0,0,0.6)',
              }}
            >
              {/* Top-Right Label inside/corner of box per Immersive UI theme */}
              <span
                className={`absolute top-2 right-3 sm:top-3 sm:right-4 text-[#888888] group-hover:text-white text-sm sm:text-lg tracking-normal select-none transition-colors ${fontClass}`}
              >
                {unit.label}
              </span>

              <span
                className={`text-5xl sm:text-7xl md:text-8xl text-white font-bold select-none leading-none tracking-tighter group-hover:scale-105 transition-transform ${fontClass}`}
              >
                {unit.value}
              </span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

