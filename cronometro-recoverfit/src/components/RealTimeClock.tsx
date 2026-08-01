import React, { useState, useEffect } from 'react';
import { FontOption } from '../types';

interface RealTimeClockProps {
  fontStyle: FontOption;
}

export const RealTimeClock: React.FC<RealTimeClockProps> = ({ fontStyle }) => {
  const [time, setTime] = useState<Date>(new Date());
  const [is24Hour, setIs24Hour] = useState<boolean>(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const fontClass =
    fontStyle === 'handwritten'
      ? 'font-handwritten'
      : fontStyle === 'caveat'
      ? 'font-casual'
      : 'font-comic';

  const formatTime = (date: Date) => {
    if (is24Hour) {
      return date.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      });
    } else {
      return date.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
      });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center my-4 sm:my-6">
      <button
        onClick={() => setIs24Hour(!is24Hour)}
        title="Haz clic para cambiar formato (12h / 24h)"
        className="bg-[#1c1c1e] hover:bg-[#252528] transition-colors border border-white/5 rounded-2xl px-10 py-3.5 sm:px-16 sm:py-4 shadow-[0_4px_20px_rgba(0,0,0,0.4)] text-center cursor-pointer group"
      >
        <span
          className={`text-2xl sm:text-3xl text-[#a1a1a6] group-hover:text-white font-medium select-none tracking-widest ${fontClass}`}
        >
          {formatTime(time)}
        </span>
      </button>
    </div>
  );
};
