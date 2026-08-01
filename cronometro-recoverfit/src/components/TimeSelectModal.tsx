import React, { useState } from 'react';
import { FontOption } from '../types';
import { ChevronUp, ChevronDown } from 'lucide-react';

interface TimeSelectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (hours: number, minutes: number, seconds: number) => void;
  initialHours: number;
  initialMinutes: number;
  initialSeconds: number;
  fontStyle: FontOption;
}

export const TimeSelectModal: React.FC<TimeSelectModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  initialHours,
  initialMinutes,
  initialSeconds,
  fontStyle,
}) => {
  if (!isOpen) return null;

  const [hours, setHours] = useState<number>(initialHours);
  const [minutes, setMinutes] = useState<number>(initialMinutes);
  const [seconds, setSeconds] = useState<number>(initialSeconds);

  const fontClass =
    fontStyle === 'handwritten'
      ? 'font-handwritten'
      : fontStyle === 'caveat'
      ? 'font-casual'
      : 'font-comic';

  const handleHoursChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    if (isNaN(val)) setHours(0);
    else setHours(Math.max(0, Math.min(99, val)));
  };

  const handleMinutesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    if (isNaN(val)) setMinutes(0);
    else setMinutes(Math.max(0, Math.min(59, val)));
  };

  const handleSecondsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    if (isNaN(val)) setSeconds(0);
    else setSeconds(Math.max(0, Math.min(59, val)));
  };

  const handleAccept = () => {
    onConfirm(hours, minutes, seconds);
  };

  const pad = (num: number) => String(num).padStart(2, '0');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4 animate-fadeIn">
      {/* Modal Box matching image_1.png styling */}
      <div className="w-full max-w-lg bg-[#535e6c] border border-white/10 rounded-3xl p-6 sm:p-8 shadow-[0_20px_50px_rgba(0,0,0,0.8)] relative flex flex-col items-center">
        {/* Spinner Inputs Container */}
        <div className="w-full grid grid-cols-3 gap-3 sm:gap-4 mb-8">
          {/* Horas Column */}
          <div className="flex flex-col items-center">
            <span
              className={`text-gray-200 text-lg sm:text-2xl mb-2 font-medium select-none ${fontClass}`}
            >
              Horas
            </span>

            <div className="relative w-full bg-[#3d4653] border-2 border-sky-400/80 rounded-xl flex items-center px-2 py-1.5 shadow-inner">
              <input
                type="number"
                min={0}
                max={99}
                value={pad(hours)}
                onChange={handleHoursChange}
                className={`w-full bg-transparent text-center text-2xl sm:text-3xl text-white font-bold outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none ${fontClass}`}
              />
              <div className="flex flex-col justify-between h-full pl-1">
                <button
                  type="button"
                  onClick={() => setHours((h) => Math.min(99, h + 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronUp size={16} />
                </button>
                <button
                  type="button"
                  onClick={() => setHours((h) => Math.max(0, h - 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronDown size={16} />
                </button>
              </div>
            </div>

            <span
              className={`text-gray-300 text-sm sm:text-base mt-1.5 select-none ${fontClass}`}
            >
              (0-99)
            </span>
          </div>

          {/* Minutos Column */}
          <div className="flex flex-col items-center">
            <span
              className={`text-gray-200 text-lg sm:text-2xl mb-2 font-medium select-none ${fontClass}`}
            >
              Minutos
            </span>

            <div className="relative w-full bg-[#3d4653] border border-gray-400/40 rounded-xl flex items-center px-2 py-1.5 shadow-inner">
              <input
                type="number"
                min={0}
                max={59}
                value={pad(minutes)}
                onChange={handleMinutesChange}
                className={`w-full bg-transparent text-center text-2xl sm:text-3xl text-white font-bold outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none ${fontClass}`}
              />
              <div className="flex flex-col justify-between h-full pl-1">
                <button
                  type="button"
                  onClick={() => setMinutes((m) => Math.min(59, m + 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronUp size={16} />
                </button>
                <button
                  type="button"
                  onClick={() => setMinutes((m) => Math.max(0, m - 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronDown size={16} />
                </button>
              </div>
            </div>

            <span
              className={`text-gray-300 text-sm sm:text-base mt-1.5 select-none ${fontClass}`}
            >
              (0-59)
            </span>
          </div>

          {/* Segundos Column */}
          <div className="flex flex-col items-center">
            <span
              className={`text-gray-200 text-lg sm:text-2xl mb-2 font-medium select-none ${fontClass}`}
            >
              Segundos
            </span>

            <div className="relative w-full bg-[#3d4653] border border-gray-400/40 rounded-xl flex items-center px-2 py-1.5 shadow-inner">
              <input
                type="number"
                min={0}
                max={59}
                value={pad(seconds)}
                onChange={handleSecondsChange}
                className={`w-full bg-transparent text-center text-2xl sm:text-3xl text-white font-bold outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none ${fontClass}`}
              />
              <div className="flex flex-col justify-between h-full pl-1">
                <button
                  type="button"
                  onClick={() => setSeconds((s) => Math.min(59, s + 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronUp size={16} />
                </button>
                <button
                  type="button"
                  onClick={() => setSeconds((s) => Math.max(0, s - 1))}
                  className="p-0.5 text-gray-300 hover:text-white transition-colors cursor-pointer"
                >
                  <ChevronDown size={16} />
                </button>
              </div>
            </div>

            <span
              className={`text-gray-300 text-sm sm:text-base mt-1.5 select-none ${fontClass}`}
            >
              (0-59)
            </span>
          </div>
        </div>

        {/* Modal Buttons (Aceptar, Cancelar) */}
        <div className="w-full flex items-center justify-between gap-4">
          <button
            onClick={handleAccept}
            className={`flex-1 py-3 sm:py-3.5 bg-[#8b99aa] hover:bg-[#9aaabc] active:scale-98 text-[#12161b] font-bold text-2xl sm:text-3xl rounded-2xl shadow-lg transition-all border border-white/20 select-none cursor-pointer ${fontClass}`}
          >
            Aceptar
          </button>
          <button
            onClick={onClose}
            className={`flex-1 py-3 sm:py-3.5 bg-[#8b99aa] hover:bg-[#9aaabc] active:scale-98 text-[#12161b] font-bold text-2xl sm:text-3xl rounded-2xl shadow-lg transition-all border border-white/20 select-none cursor-pointer ${fontClass}`}
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};
