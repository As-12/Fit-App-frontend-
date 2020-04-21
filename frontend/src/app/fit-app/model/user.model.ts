export interface User {
  readonly id?: string;
  name?: string;
  city?: string;
  state?: string;
  height?: number;
  target_weight?: number;
}

export interface UserList {
  users: Array<User>;
  count: number;
}
