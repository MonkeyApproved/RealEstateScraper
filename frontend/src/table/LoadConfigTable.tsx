import { AppstoreOutlined, HomeOutlined } from '@ant-design/icons';
import { Table } from 'antd';
import Column from 'antd/lib/table/Column';
import { geo_location_ids, LoadConfig } from '../requests/data_manager';

export interface LoadConfigTableProps {
  loadConfig: LoadConfig[];
}

export default function LoadConfigTable({ loadConfig }: LoadConfigTableProps) {
  const renderType = (value: string) => {
    if (value === 're_residence') {
      return (
        <>
          <HomeOutlined />
          <span style={{ paddingLeft: 10 }}>Residence</span>
        </>
      );
    }
    return (
      <>
        <AppstoreOutlined />
        <span style={{ paddingLeft: 10 }}>Land</span>
      </>
    );
  };

  const renderFrequency = (value: number) => {
    if (value === 1) {
      return <span>Hourly</span>;
    } else if (value === 24) {
      return <span>Daily</span>;
    } else if (value === 24 * 7) {
      return <span>Weekly</span>;
    }
    return <span>{`every ${value}h`}</span>;
  };

  const renderLocation = (value: string) => {
    if (geo_location_ids[value]) {
      return <span>{geo_location_ids[value]}</span>;
    }
    return <span>unknown</span>;
  };

  return (
    <Table dataSource={loadConfig}>
      <Column title="Name" dataIndex="config_name" key="config_name" />
      <Column title="Frequency" dataIndex="frequency" key="frequency" render={renderFrequency} />
      <Column
        title="Location"
        dataIndex="geo_place_id"
        key="geo_place_id"
        render={renderLocation}
      />
      <Column title="Type" dataIndex="item_type" key="item_type" render={renderType} />
    </Table>
  );
}
