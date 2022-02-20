import { useEffect, useState } from 'react';
import styles from './Tabs.module.css';
import { getXeResult, XeResult } from '../requests/xe_properties';
import { message } from 'antd';
import PropertiesTable from '../table/PropertiesTable';

export default function PropertiesTab() {
  const [properties, setProperties] = useState<XeResult[]>([]);
  const [count, setCount] = useState<number>(0);

  useEffect(() => {
    getXeResult()
      .then((response) => {
        setProperties(response.data.results);
        setCount(response.data.count);
      })
      .catch((error) => {
        message.error(`Failed to GET Xe Results: ${error}`);
      });
  }, []);

  return (
    <div className={styles.content}>
      <PropertiesTable propertyList={properties} count={count} />
    </div>
  );
}
