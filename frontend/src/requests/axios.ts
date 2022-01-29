import axios, { AxiosResponse } from 'axios';

const HOST = 'http://localhost:8000/';

export interface Test {
  key1: string;
  key2: string;
}

export async function getTest(): Promise<AxiosResponse<Test>> {
  return axios.get(`${HOST}/test`);
}
