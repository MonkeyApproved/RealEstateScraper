import { Button, Table, TablePaginationConfig } from 'antd';
import Modal from 'antd/lib/modal/Modal';
import Column from 'antd/lib/table/Column';
import { FilterValue, SorterResult } from 'antd/lib/table/interface';
import ApartmentDetails from '../pages/ApartmentDetails';
import { Details, TableSettings, XeResult } from '../requests/xe_properties';
import { renderDate } from './tableHelper';
import styles from './Table.module.css';
import { useState } from 'react';

export interface ApartmentTableProps {
  propertyList: XeResult[];
  settings: TableSettings;
  setSettings: (value: TableSettings) => void;
}

export default function ApartmentTable({
  propertyList,
  settings,
  setSettings,
}: ApartmentTableProps) {
  const [showDetails, setShowDetails] = useState<boolean>(false);
  const [detailsId, setDetailsId] = useState<number>(0);

  const renderRooms = (value: Details) => {
    return <span>{`${value.bathrooms || 0} bath, ${value.bedrooms || 0} bed`}</span>;
  };

  const onRowClick = (record: XeResult) => {
    setDetailsId(record.xe_id);
    setShowDetails(true);
  };

  const tableChange = (
    pagination: TablePaginationConfig,
    filters: Record<string, FilterValue | null>,
    sorter: SorterResult<XeResult> | SorterResult<XeResult>[],
  ) => {
    if (Array.isArray(sorter)) {
      sorter = sorter[0];
    }
    const page_number = (pagination.current || 1) - 1;
    const page_size = pagination.pageSize || 20;
    let ordering = '';
    if (sorter.columnKey && sorter.order) {
      ordering = `&ordering=${sorter.order === 'ascend' ? '' : '-'}${sorter.columnKey}`;
    }
    setSettings({
      page: pagination.current || 1,
      count: settings.count,
      limit: page_size,
      offset: page_number * page_size,
      ordering: ordering,
      filter: '&type=re_residence',
    });
  };

  const closeDetails = () => {
    setShowDetails(false);
    setDetailsId(0);
  };

  return (
    <>
      <Table
        dataSource={propertyList}
        pagination={{ pageSize: 20, total: settings.count, simple: true, current: settings.page }}
        onRow={(record) => {
          return {
            onClick: () => onRowClick(record),
          };
        }}
        onChange={tableChange}
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
          sorter={true}
        />
      </Table>
      <Modal
        style={{ top: 20 }}
        width={'90vw'}
        visible={showDetails}
        className={styles.content}
        footer={
          <Button key="back" onClick={closeDetails}>
            Back
          </Button>
        }
        onCancel={closeDetails}
      >
        <ApartmentDetails xe_id={detailsId} />
      </Modal>
    </>
  );
}
