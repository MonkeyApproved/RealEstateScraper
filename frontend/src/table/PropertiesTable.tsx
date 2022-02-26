import { Table, TablePaginationConfig } from 'antd';
import Column from 'antd/lib/table/Column';
import { FilterValue, SorterResult } from 'antd/lib/table/interface';
import { useNavigate } from 'react-router-dom';
import { Details, XeResult } from '../requests/xe_properties';
import { renderDate } from './tableHelper';

export interface PropertyTableSettings {
  count: number;
  limit: number;
  offset: number;
  ordering: string;
  filter: string;
}

export interface PropertiesTableProps {
  propertyList: XeResult[];
  settings: PropertyTableSettings;
  setSettings: (value: PropertyTableSettings) => void;
}

export default function PropertiesTable({
  propertyList,
  settings,
  setSettings,
}: PropertiesTableProps) {
  const navigate = useNavigate();

  const renderRooms = (value: Details) => {
    return <span>{`${value.bathrooms || 0} bath, ${value.bedrooms || 0} bed`}</span>;
  };

  const onRowClick = (record: XeResult) => {
    navigate(`/details/${record.xe_id}`);
  };

  const tableChange = (
    pagination: TablePaginationConfig,
    filters: Record<string, FilterValue | null>,
    sorter: SorterResult<XeResult> | SorterResult<XeResult>[],
  ) => {
    if (Array.isArray(sorter)) {
      sorter = sorter[0];
    }
    const page_number = (pagination.current || 1) - 1;
    const page_size = pagination.pageSize || 20;
    let ordering = '';
    if (sorter.columnKey && sorter.order) {
      ordering = `&ordering=${sorter.order === 'ascend' ? '' : '-'}${sorter.columnKey}`;
    }
    setSettings({
      count: settings.count,
      limit: page_size,
      offset: page_number * page_size,
      ordering: ordering,
      filter: '',
    });
  };

  return (
    <Table
      dataSource={propertyList}
      pagination={{ pageSize: 20, total: settings.count, simple: true }}
      onRow={(record) => {
        return {
          onClick: () => onRowClick(record),
        };
      }}
      onChange={tableChange}
    >
      <Column title="Area" dataIndex={['details', 'area']} key="area" />
      <Column title="Price" dataIndex={['details', 'price_total']} key="price_total" />
      <Column title="Size" dataIndex={['details', 'size_sqm']} key="size_sqm" />
      <Column title="Year" dataIndex={['details', 'construction_year']} key="year" />
      <Column title="Owner" dataIndex="owner" key="owner" />
      <Column title="Rooms" dataIndex="details" key="details" render={renderRooms} />
      <Column
        title="First parsed"
        dataIndex="first_parsed_on"
        key="first_parsed_on"
        render={renderDate}
      />
      <Column
        title="Last parsed"
        dataIndex="last_parsed_on"
        key="last_parsed_on"
        render={renderDate}
        sorter={true}
      />
    </Table>
  );
}
