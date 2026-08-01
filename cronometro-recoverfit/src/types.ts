export type StopwatchStatus = 'idle' | 'running' | 'paused';
export type TimerMode = 'stopwatch' | 'countdown';

export type FontOption = 'handwritten' | 'caveat' | 'comic';

export interface LapTime {
  id: number;
  time: number;
  formattedTime: string;
}
