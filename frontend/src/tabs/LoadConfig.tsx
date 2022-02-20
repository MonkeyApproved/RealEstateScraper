import { useEffect, useState } from 'react';
import styles from './Tabs.module.css';
import LoadConfigTable from '../table/LoadConfigTable';
import { getLoadConfig, LoadConfig } from '../requests/data_manager';
import { message } from 'antd';

export default function LoadConfigTab() {
  const [loadConfig, setLoadConfig] = useState<LoadConfig[]>([]);

  useEffect(() => {
    getLoadConfig()
      .then((response) => {
        setLoadConfig(response.data.results);
      })
      .catch((error) => {
        message.error(`Failed to get load_config: ${error}`);
      });
  }, []);

  return (
    <div className={styles.content}>
      <LoadConfigTable loadConfig={loadConfig} />
    </div>
  );
}
