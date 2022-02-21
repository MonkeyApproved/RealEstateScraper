import { Table } from 'antd';
import Column from 'antd/lib/table/Column';
import { useNavigate } from 'react-router-dom';
import { Details, XeResult } from '../requests/xe_properties';
import { renderDate } from './tableHelper';

export interface PropertiesTableProps {
  propertyList: XeResult[];
  count: number;
  setPage: (value: number) => void;
}

export default function PropertiesTable({ propertyList, count, setPage }: PropertiesTableProps) {
  const navigate = useNavigate();

  const renderRooms = (value: Details) => {
    return <span>{`${value.bathrooms || 0} bath, ${value.bedrooms || 0} bed`}</span>;
  };

  const onRowClick = (record: XeResult) => {
    navigate(`/details/${record.xe_id}`);
  };

  const pageChange = (page: number) => {
    setPage(page);
  };

  return (
    <Table
      dataSource={propertyList}
      pagination={{ pageSize: 20, total: count, simple: true, onChange: pageChange }}
      onRow={(record) => {
        return {
          onClick: () => onRowClick(record),
        };
      }}
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
      />
    </Table>
  );
}
