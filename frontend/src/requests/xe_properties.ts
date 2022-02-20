import axios, { AxiosResponse } from 'axios';
import { Pagination } from './helper';

const HOST = 'http://localhost:8001/properties';

export interface XeResult {
  id: number;
  xe_id: number;
  first_parsed_on: string;
  last_parsed_on: string;
  created: string;
  modified: string;
  owner: string;
  location: Location;
  details: Details;
}

export interface Details {
  area: string;
  bathrooms: number;
  bedrooms: number;
  commercial: boolean;
  construction_year: number;
  description: string;
  id: number;
  item_type: string;
  price_sqm: number;
  price_total: number;
  property_type: string;
  size_sqm: number;
}

export interface Location {
  id: number;
  latitude: string;
  longitude: string;
}

export async function getXeResult(): Promise<AxiosResponse<Pagination<XeResult>>> {
  return axios.get(`${HOST}/xe_result/`);
}
