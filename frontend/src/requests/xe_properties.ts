import axios, { AxiosResponse } from 'axios';
import { BASE_URL, Pagination } from './helper';

const HOST = `${BASE_URL}/properties`;

export interface XeResult {
  id: number;
  xe_id: number;
  first_parsed_on: string;
  last_parsed_on: string;
  url: string;
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

export interface Owner {
  id: number;
  account_id: number;
  email: string;
  address: string;
  ref_id: string;
  company_title: string;
  active_ads: number;
}

export interface Metrics {
  id: number;
  date: string;
  xe_id: number;
  saves: number;
  visits: number;
}

export interface Image {
  xe_id: number;
  small: string;
  medium: string;
  big: string;
}

export interface GetDetails {
  xe_result: XeResult[];
  details: Details[];
  location: Location[];
  owner: Owner[];
  metrics: Metrics[];
  images: Image[];
}

export interface TableSettings {
  page: number;
  count: number;
  limit: number;
  offset: number;
  ordering: string;
  filter: string;
}

export async function getXeResult({
  offset,
  limit,
  ordering,
  filter,
}: TableSettings): Promise<AxiosResponse<Pagination<XeResult>>> {
  const pagination = `?limit=${limit}&offset=${offset}`;
  return axios.get(`${HOST}/xe_result/${pagination}${ordering}${filter}`);
}

export async function getDetails(xe_id: number): Promise<AxiosResponse<GetDetails>> {
  return axios.get(`${HOST}/details/${xe_id}`);
}
