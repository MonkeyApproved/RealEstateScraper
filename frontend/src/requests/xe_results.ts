import axios, { AxiosResponse } from 'axios';

const HOST = 'http://localhost:8001/api';

export interface XeResult {
  id: number;
  xe_id: number;
  first_parsed_on: string;
  last_parsed_on: string;
  created: string;
  modified: string;
  owner: number;
  location: number;
  details: number;
}

export async function getXeResult(): Promise<AxiosResponse<XeResult[]>> {
  return axios.get(`${HOST}/xe_result/`);
}
