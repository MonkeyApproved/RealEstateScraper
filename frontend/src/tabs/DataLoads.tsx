import { useEffect, useState } from 'react';
import styles from './Tabs.module.css';
import { getDataLoads, DataLoad } from '../requests/data_manager';
import { message } from 'antd';
import DataLoadsTable from '../table/DataLoadsTable';

export default function DataLoadsTab() {
  const [dataLoad, setDataLoad] = useState<DataLoad[]>([]);

  useEffect(() => {
    getDataLoads()
      .then((response) => {
        setDataLoad(response.data.results);
      })
      .catch((error) => {
        message.error(`Failed to get load_config: ${error}`);
      });
  }, []);

  return (
    <div className={styles.content}>
      <DataLoadsTable dataLoad={dataLoad} />
    </div>
  );
}
