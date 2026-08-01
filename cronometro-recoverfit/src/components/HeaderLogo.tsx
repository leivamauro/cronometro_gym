import React from 'react';

export const HeaderLogo: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center pt-2 pb-6 select-none">
      {/* SVG Icon matching the RF Metallic Emblem */}
      <div className="relative mb-3 w-24 h-16 flex items-center justify-center">
        <svg
          viewBox="0 0 200 120"
          className="w-full h-full filter drop-shadow-[0_2px_8px_rgba(255,255,255,0.15)]"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Silver metallic gradient */}
            <linearGradient id="silver-metal" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="35%" stopColor="#C0C0C0" />
              <stop offset="50%" stopColor="#E8E8E8" />
              <stop offset="70%" stopColor="#8A8A8A" />
              <stop offset="100%" stopColor="#DFDFDF" />
            </linearGradient>
            <linearGradient id="silver-dark" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#737373" />
              <stop offset="50%" stopColor="#D4D4D4" />
              <stop offset="100%" stopColor="#A3A3A3" />
            </linearGradient>
          </defs>

          {/* Wing/Chevron Shield Structure representing RF */}
          {/* Left Wing R section */}
          <path
            d="M 20 20 L 92 20 L 78 45 L 35 45 Z"
            fill="url(#silver-metal)"
          />
          <path
            d="M 35 45 L 85 45 L 75 62 L 50 62 Z"
            fill="url(#silver-dark)"
          />
          <path
            d="M 20 20 L 55 62 L 70 62 L 40 20 Z"
            fill="url(#silver-metal)"
          />

          {/* Right Wing F section */}
          <path
            d="M 180 20 L 108 20 L 122 45 L 165 45 Z"
            fill="url(#silver-metal)"
          />
          <path
            d="M 165 45 L 115 45 L 125 62 L 150 62 Z"
            fill="url(#silver-dark)"
          />
          <path
            d="M 180 20 L 145 62 L 130 62 L 160 20 Z"
            fill="url(#silver-metal)"
          />

          {/* Central Downward Shield Tip (RF Center V) */}
          <path
            d="M 75 65 L 125 65 L 100 110 Z"
            fill="url(#silver-metal)"
          />
          <path
            d="M 85 68 L 115 68 L 100 98 Z"
            fill="url(#silver-dark)"
          />
        </svg>
      </div>

      {/* Brand Text */}
      <h1 className="font-brand text-2xl md:text-3xl font-extrabold tracking-[0.25em] text-white uppercase text-center drop-shadow-sm pb-2 border-b border-zinc-800/80 mb-1 w-full max-w-xs sm:max-w-md">
        RECOVERFIT
      </h1>
      <p className="font-brand text-[10px] md:text-xs tracking-[0.3em] text-zinc-500 uppercase text-center font-semibold">
        RECUPERACIÓN Y ENTRENAMIENTO
      </p>
    </div>
  );
};
