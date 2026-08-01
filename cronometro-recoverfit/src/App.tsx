import React, { useState, useEffect, useRef, useCallback } from 'react';
import { HeaderLogo } from './components/HeaderLogo';
import { StopwatchDisplay } from './components/StopwatchDisplay';
import { RealTimeClock } from './components/RealTimeClock';
import { ControlButtons } from './components/ControlButtons';
import { ExtraSettings } from './components/ExtraSettings';
import { LapHistory } from './components/LapHistory';
import { TimeSelectModal } from './components/TimeSelectModal';
import { StopwatchStatus, TimerMode, FontOption, LapTime } from './types';
import { playBeep } from './utils/audio';

export default function App() {
  const [status, setStatus] = useState<StopwatchStatus>('idle');
  const [mode, setMode] = useState<TimerMode>('stopwatch');

  // Count UP Stopwatch State
  const [elapsedMs, setElapsedMs] = useState<number>(0);

  // Count DOWN Timer State
  const [targetCountdownMs, setTargetCountdownMs] = useState<number>(0);
  const [remainingCountdownMs, setRemainingCountdownMs] = useState<number>(0);

  // UI State
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [fontStyle, setFontStyle] = useState<FontOption>('handwritten');
  const [soundEnabled, setSoundEnabled] = useState<boolean>(true);
  const [laps, setLaps] = useState<LapTime[]>([]);
  const [showLaps, setShowLaps] = useState<boolean>(false);

  // References for precision animation loop
  const startTimeRef = useRef<number>(0);
  const accumulatedTimeRef = useRef<number>(0);
  const animFrameRef = useRef<number | null>(null);

  const modeRef = useRef<TimerMode>('stopwatch');
  const targetMsRef = useRef<number>(0);

  // Synchronize refs with state
  useEffect(() => {
    modeRef.current = mode;
  }, [mode]);

  useEffect(() => {
    targetMsRef.current = targetCountdownMs;
  }, [targetCountdownMs]);

  // High Precision Animation Frame Timer Loop
  const updateTimer = useCallback(() => {
    if (startTimeRef.current > 0) {
      const now = Date.now();
      const currentDelta = now - startTimeRef.current;
      const totalAccumulated = accumulatedTimeRef.current + currentDelta;

      if (modeRef.current === 'stopwatch') {
        setElapsedMs(totalAccumulated);
        animFrameRef.current = requestAnimationFrame(updateTimer);
      } else {
        // Countdown Mode
        const rem = targetMsRef.current - totalAccumulated;
        if (rem <= 0) {
          setRemainingCountdownMs(0);
          setStatus('idle');
          if (soundEnabled) playBeep('reset');
          if (animFrameRef.current) {
            cancelAnimationFrame(animFrameRef.current);
            animFrameRef.current = null;
          }
        } else {
          setRemainingCountdownMs(rem);
          animFrameRef.current = requestAnimationFrame(updateTimer);
        }
      }
    }
  }, [soundEnabled]);

  // Handle Start / Resume
  const handleStart = () => {
    if (status === 'running') return;

    if (soundEnabled) playBeep('start');

    if (mode === 'countdown') {
      // If countdown finished at 0, restart from target time
      if (remainingCountdownMs <= 0 && targetCountdownMs > 0) {
        accumulatedTimeRef.current = 0;
        setRemainingCountdownMs(targetCountdownMs);
      }
    }

    startTimeRef.current = Date.now();
    setStatus('running');
    animFrameRef.current = requestAnimationFrame(updateTimer);
  };

  // Handle Pause
  const handlePause = () => {
    if (status !== 'running') return;

    if (soundEnabled) playBeep('pause');
    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current);
      animFrameRef.current = null;
    }

    const now = Date.now();
    accumulatedTimeRef.current += now - startTimeRef.current;
    startTimeRef.current = 0;
    setStatus('paused');
  };

  // Handle Reset (Always resets back to MODO CRONÓMETRO 00:00:00)
  const handleReset = () => {
    if (soundEnabled) playBeep('reset');
    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current);
      animFrameRef.current = null;
    }

    startTimeRef.current = 0;
    accumulatedTimeRef.current = 0;
    setElapsedMs(0);
    setTargetCountdownMs(0);
    setRemainingCountdownMs(0);
    setMode('stopwatch');
    setStatus('idle');
  };

  // Handle Modal Confirm Time Selection (Sets Countdown Mode)
  const handleConfirmModalTime = (h: number, m: number, s: number) => {
    const totalMs = (h * 3600 + m * 60 + s) * 1000;

    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current);
      animFrameRef.current = null;
    }

    startTimeRef.current = 0;
    accumulatedTimeRef.current = 0;

    if (totalMs > 0) {
      setMode('countdown');
      setTargetCountdownMs(totalMs);
      setRemainingCountdownMs(totalMs);
      setStatus('idle');
    } else {
      // Set to 00:00:00 = Stopwatch mode
      setMode('stopwatch');
      setElapsedMs(0);
      setTargetCountdownMs(0);
      setRemainingCountdownMs(0);
      setStatus('idle');
    }

    setIsModalOpen(false);
  };

  // Add Lap
  const handleAddLap = () => {
    const activeMs = mode === 'countdown' ? remainingCountdownMs : elapsedMs;
    if (activeMs === 0) return;
    if (soundEnabled) playBeep('tick');

    const totalSecs = Math.floor(activeMs / 1000);
    const hrs = String(Math.floor(totalSecs / 3600)).padStart(2, '0');
    const mins = String(Math.floor((totalSecs % 3600) / 60)).padStart(2, '0');
    const secs = String(Math.floor(totalSecs % 60)).padStart(2, '0');

    const formatted = `${hrs}:${mins}:${secs}`;
    const newLap: LapTime = {
      id: laps.length + 1,
      time: activeMs,
      formattedTime: formatted,
    };

    setLaps((prev) => [...prev, newLap]);
    if (!showLaps) setShowLaps(true);
  };

  const handleClearLaps = () => {
    setLaps([]);
  };

  // Cleanup animation frame on unmount
  useEffect(() => {
    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, []);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      if (e.code === 'Space') {
        e.preventDefault();
        if (status === 'running') {
          handlePause();
        } else {
          handleStart();
        }
      } else if (e.code === 'KeyR') {
        e.preventDefault();
        handleReset();
      } else if (e.code === 'KeyL' && status === 'running') {
        e.preventDefault();
        handleAddLap();
      } else if (e.code === 'KeyM') {
        e.preventDefault();
        setIsModalOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [status, soundEnabled, elapsedMs, remainingCountdownMs, mode, laps]);

  // Active time display calculation
  const activeMs = mode === 'countdown' ? remainingCountdownMs : elapsedMs;
  const totalSeconds = Math.max(0, Math.floor(activeMs / 1000));
  const displayHours = Math.floor(totalSeconds / 3600);
  const displayMinutes = Math.floor((totalSeconds % 3600) / 60);
  const displaySeconds = Math.floor(totalSeconds % 60);

  // Modal Initial Values
  const modalInitialSecs = Math.floor(
    (mode === 'countdown' && targetCountdownMs > 0 ? targetCountdownMs : elapsedMs) / 1000
  );
  const modalInitialHours = Math.floor(modalInitialSecs / 3600);
  const modalInitialMinutes = Math.floor((modalInitialSecs % 3600) / 60);
  const modalInitialSeconds = Math.floor(modalInitialSecs % 60);

  return (
    <div className="min-h-screen w-full bg-black text-white flex flex-col justify-between py-6 px-4 selection:bg-gray-800">
      {/* Outer framing centered container replicating tablet / app screen design */}
      <div className="w-full max-w-3xl mx-auto my-auto bg-black rounded-3xl p-4 sm:p-8 border border-gray-900 shadow-[0_0_50px_rgba(0,0,0,0.9)] relative flex flex-col justify-between min-h-[620px]">
        {/* Header with Logo */}
        <HeaderLogo />

        {/* Stopwatch Display (3 big square boxes - Clickable to open modal) */}
        <StopwatchDisplay
          hours={displayHours}
          minutes={displayMinutes}
          seconds={displaySeconds}
          fontStyle={fontStyle}
          onOpenModal={() => setIsModalOpen(true)}
          mode={mode}
        />

        {/* Real Time System Clock Box */}
        <RealTimeClock fontStyle={fontStyle} />

        {/* Primary Action Buttons (Iniciar, Pausar, Reiniciar) */}
        <ControlButtons
          status={status}
          onStart={handleStart}
          onPause={handlePause}
          onReset={handleReset}
          fontStyle={fontStyle}
        />

        {/* Lap History Panel (Optional collapsible) */}
        {showLaps && (
          <LapHistory
            laps={laps}
            onAddLap={handleAddLap}
            onClearLaps={handleClearLaps}
            isRunning={status === 'running'}
            fontStyle={fontStyle}
          />
        )}

        {/* Extra Settings & Font Selector */}
        <ExtraSettings
          fontStyle={fontStyle}
          setFontStyle={setFontStyle}
          soundEnabled={soundEnabled}
          setSoundEnabled={setSoundEnabled}
          onAddLap={handleAddLap}
          showLaps={showLaps}
          setShowLaps={setShowLaps}
          onResetApp={handleReset}
        />
      </div>

      {/* Time Selection Modal */}
      <TimeSelectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleConfirmModalTime}
        initialHours={modalInitialHours}
        initialMinutes={modalInitialMinutes}
        initialSeconds={modalInitialSeconds}
        fontStyle={fontStyle}
      />
    </div>
  );
}

