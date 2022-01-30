import { Table, message } from 'antd';
import { useEffect, useState } from 'react';
import { getXeResult, XeResult } from '../requests/xe_results';

export interface PropertiesTableProps {
  propertyList: XeResult[];
}

export default function PropertiesTable() {
  const [data, setData] = useState<XeResult[]>([]);

  useEffect(() => {
    getXeResult()
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        message.error(`Failed to load Xe Results: ${error}`);
      });
  }, []);

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Xe Id',
      dataIndex: 'xe_id',
      key: 'xe_id',
    },
    {
      title: 'First parsed',
      dataIndex: 'first_parsed_on',
      key: 'first_parsed_on',
    },
    {
      title: 'Last parsed',
      dataIndex: 'last_parsed_on',
      key: 'last_parsed_on',
    },
  ];

  return <Table dataSource={data} columns={columns} />;
}
