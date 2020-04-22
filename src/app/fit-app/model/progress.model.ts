export interface Progress {
  user_id: string;
  track_date: Date | string;
  weight: number;
  mood: string;
  diet: string;
}

export interface ProgressList {
  user_id: string;
  progresses: Array<Progress>;
  count: number;
}
