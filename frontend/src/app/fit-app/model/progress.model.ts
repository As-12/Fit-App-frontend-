export interface Progress {
  user_id: string;
  track_date: Date;
  weight: string;
  mood: string;
  diet: string;
}

export interface ProgressList {
  user_id: string;
  progresses: Array<Progress>;
  count: number;
}
