import React from 'react';
import { LapTime, FontOption } from '../types';
import { Trash2, Flag } from 'lucide-react';

interface LapHistoryProps {
  laps: LapTime[];
  onAddLap: () => void;
  onClearLaps: () => void;
  isRunning: boolean;
  fontStyle: FontOption;
}

export const LapHistory: React.FC<LapHistoryProps> = ({
  laps,
  onAddLap,
  onClearLaps,
  isRunning,
  fontStyle,
}) => {
  const fontClass =
    fontStyle === 'handwritten'
      ? 'font-handwritten'
      : fontStyle === 'caveat'
      ? 'font-casual'
      : 'font-comic';

  return (
    <div className="w-full max-w-2xl mx-auto px-2 mt-4 animate-fadeIn">
      <div className="bg-[#1e232a] border border-[#2d343f] rounded-2xl p-4 shadow-xl">
        <div className="flex items-center justify-between pb-3 mb-3 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <Flag size={18} className="text-gray-400" />
            <h3 className="text-gray-300 font-semibold text-sm uppercase tracking-wider">
              Historial de Vueltas / Laps ({laps.length})
            </h3>
          </div>

          <div className="flex items-center gap-2">
            {isRunning && (
              <button
                onClick={onAddLap}
                className="px-3 py-1 bg-[#3a4452] hover:bg-[#485466] text-white text-xs font-medium rounded-lg transition-colors flex items-center gap-1 cursor-pointer"
              >
                + Registrar Vuelta
              </button>
            )}
            {laps.length > 0 && (
              <button
                onClick={onClearLaps}
                className="p-1.5 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors cursor-pointer"
                title="Limpiar vueltas"
              >
                <Trash2 size={16} />
              </button>
            )}
          </div>
        </div>

        {laps.length === 0 ? (
          <p className="text-center text-gray-500 text-xs py-4 italic">
            No hay vueltas registradas. {isRunning ? 'Haz clic en "+ Registrar Vuelta" durante la carrera.' : 'Inicia el cronómetro para marcar tiempos.'}
          </p>
        ) : (
          <div className="max-h-48 overflow-y-auto pr-1 space-y-1.5 custom-scrollbar">
            {laps
              .slice()
              .reverse()
              .map((lap) => (
                <div
                  key={lap.id}
                  className="flex items-center justify-between py-2 px-3 bg-[#282f39] hover:bg-[#303844] rounded-xl text-gray-300 text-base"
                >
                  <span className="text-gray-400 text-xs font-mono font-bold">
                    Vuelta #{lap.id}
                  </span>
                  <span className={`text-xl font-bold text-gray-100 ${fontClass}`}>
                    {lap.formattedTime}
                  </span>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
};
