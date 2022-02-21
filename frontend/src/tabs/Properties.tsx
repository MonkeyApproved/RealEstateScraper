import styles from './Tabs.module.css';
import PropertiesTable, { PropertiesTableProps } from '../table/PropertiesTable';

export default function PropertiesTab({ propertyList, count, setPage }: PropertiesTableProps) {
  return (
    <div className={styles.content}>
      <PropertiesTable propertyList={propertyList} count={count} setPage={setPage} />
    </div>
  );
}
