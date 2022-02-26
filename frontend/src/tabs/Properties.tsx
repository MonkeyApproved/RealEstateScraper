import styles from './Tabs.module.css';
import PropertiesTable, { PropertiesTableProps } from '../table/PropertiesTable';

export default function PropertiesTab(props: PropertiesTableProps) {
  return (
    <div className={styles.content}>
      <PropertiesTable
        propertyList={props.propertyList}
        settings={props.settings}
        setSettings={props.setSettings}
      />
    </div>
  );
}
