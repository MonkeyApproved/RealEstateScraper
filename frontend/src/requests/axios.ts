import axios, { AxiosResponse } from 'axios';

const HOST = 'http://localhost:8001/api';

export interface Test {
  key1: string;
  key2: string;
}

export async function getXeResult(): Promise<AxiosResponse<Test>> {
  return axios.get(`${HOST}/xe_result/`);
}
