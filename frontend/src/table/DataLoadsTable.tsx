import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { Table } from 'antd';
import Column from 'antd/lib/table/Column';
import { DataLoad } from '../requests/data_manager';
import { renderDate } from './tableHelper';

export interface DataLoadTableProps {
  dataLoad: DataLoad[];
}

export default function DataLoadsTable({ dataLoad }: DataLoadTableProps) {
  const renderCompleted = (value: boolean) => {
    return value ? <CheckCircleOutlined /> : <CloseCircleOutlined />;
  };

  return (
    <Table dataSource={dataLoad}>
      <Column title="" dataIndex="completed" key="config_name" render={renderCompleted} />
      <Column title="Config" dataIndex={['load_config', 'config_name']} key="config_name" />
      <Column title="Loaded on" dataIndex="created_on" key="config_name" render={renderDate} />
      <Column title="Total" dataIndex="count_total" key="frequency" />
      <Column title="New" dataIndex="count_new" key="frequency" />
    </Table>
  );
}
