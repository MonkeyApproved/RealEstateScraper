import axios, { AxiosResponse } from 'axios';
import { Pagination } from './helper';

const HOST = 'http://localhost:8001/manager';

export const geo_location_ids: { [name: string]: string } = {
  'ChIJ8UNwBh-9oRQR3Y1mdkU1Nic': 'Athens',
  'aj5k2hs-as3dl3k': 'Corfu',
};

export interface LoadConfig {
  id: number;
  config_name: string;
  frequency: number;
  item_type: string;
  geo_place_id: string;
  maximum_price: number | undefined;
  minimum_construction_year: number | undefined;
  minimum_size: number | undefined;
  [key: string]: number | string | undefined | null;
}

export interface DataLoad {
  id: string;
  created_on: string;
  url: string;
  count_total: string;
  count_new: string;
  completed: boolean;
  load_config: LoadConfig;
}

export async function getLoadConfig(): Promise<AxiosResponse<Pagination<LoadConfig>>> {
  return axios.get(`${HOST}/load_config/`);
}

export async function postLoadConfig(config: Omit<LoadConfig, 'id'>): Promise<AxiosResponse> {
  for (const key of Object.keys(config)) {
    if (config[key] === undefined) {
      config[key] = null;
    }
  }
  return axios.post(`${HOST}/load_config/`, config);
}

export async function getDataLoads(): Promise<AxiosResponse<Pagination<DataLoad>>> {
  return axios.get(`${HOST}/data_loads/`);
}
