import { message } from 'antd';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { GetDetails, getDetails } from '../requests/xe_properties';
import styles from './Tabs.module.css';

export default function DetailsTab() {
  const params = useParams();

  const [xeResult, setXeResult] = useState<GetDetails>();

  useEffect(() => {
    getDetails(params.propertyId || '')
      .then((response) => {
        setXeResult(response.data);
      })
      .catch((error) => {
        message.error(`Failed to get load_config: ${error}`);
      });
  }, []);

  return <div className={styles.content}>{xeResult?.details[0].description}</div>;
}
