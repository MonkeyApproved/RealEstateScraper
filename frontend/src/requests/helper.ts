export const BASE_URL = 'http://192.168.178.42:8001/api';

export interface Pagination<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
