import {
  BuildOutlined,
  EuroCircleOutlined,
  HomeOutlined,
  ReadOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { Card, Divider, message, Row, Space } from 'antd';
import { useEffect, useState } from 'react';
import { GetDetails, getDetails } from '../requests/xe_properties';
import styles from './Tabs.module.css';

export interface ApartmentDetailsProps {
  xe_id: number;
}

export default function ApartmentDetails({ xe_id }: ApartmentDetailsProps) {
  const [xeResult, setXeResult] = useState<GetDetails>();

  useEffect(() => {
    getDetails(xe_id)
      .then((response) => {
        setXeResult(response.data);
      })
      .catch((error) => {
        message.error(`Failed to get load_config: ${error}`);
      });
  }, [xe_id]);

  const get_maps_url = () => {
    const long = xeResult?.location[0].longitude || '0';
    const lat = xeResult?.location[0].latitude || '0';
    return `https://maps.google.com/maps?q=${lat}, ${long}&z=15&output=embed`;
  };

  const getImages = () => {
    return xeResult?.images.map((image) => {
      return <img src={image.small} key={image.small} alt={`property_${image.xe_id}`} />;
    });
  };

  const roomsTitle = (
    <>
      <BuildOutlined />
      <span> Rooms</span>
    </>
  );

  const priceTitle = (
    <>
      <EuroCircleOutlined />
      <span> Price</span>
    </>
  );

  const descriptionTitle = (
    <>
      <ReadOutlined />
      <span> Description</span>
    </>
  );

  const ownerTitle = (
    <>
      <UserOutlined />
      <span> Contact</span>
    </>
  );

  const buildingTitle = (
    <>
      <HomeOutlined />
      <span> Building</span>
    </>
  );

  return (
    <>
      <Divider orientation="center">DETAILS</Divider>
      <Row justify="center" align="top">
        <Space direction="horizontal" align="end">
          <Card title={buildingTitle} style={{ width: 300, height: '100%' }}>
            <p>Area: {xeResult?.details[0].area}</p>
            <p>Type: {xeResult?.details[0].property_type}</p>
            <p>Year: {xeResult?.details[0].construction_year}</p>
          </Card>
          <Card title={roomsTitle} style={{ width: 300, height: '100%' }}>
            <p>{xeResult?.details[0].bathrooms} bathrooms</p>
            <p>{xeResult?.details[0].bedrooms} bedrooms</p>
          </Card>
          <Card title={priceTitle} style={{ width: 300, height: '100%' }}>
            <p>Total: {xeResult?.details[0].price_total}€</p>
            <p>Size: {xeResult?.details[0].size_sqm}m^2</p>
            <p>Relative: {xeResult?.details[0].price_sqm}€/m^2</p>
          </Card>
          <Card title={ownerTitle} style={{ width: 300, height: '100%' }}>
            <p>Company: {xeResult?.owner[0].company_title}</p>
            <p>Email: {xeResult?.owner[0].email}</p>
            <p>#Adds: {xeResult?.owner[0].active_ads}</p>
          </Card>
        </Space>
      </Row>
      <Row justify="center" align="top" style={{ paddingTop: 10 }}>
        <Card title={descriptionTitle} style={{ width: '60%', height: '100%' }}>
          <p>{xeResult?.details[0].description}</p>
          <a href={xeResult?.xe_result[0].url} target="_blank" rel="noreferrer">
            See add on xe.gr
          </a>
        </Card>
      </Row>
      <Divider orientation="center">IMAGES</Divider>
      <Row justify="center" align="top" style={{ paddingTop: 10 }}>
        <div className={styles.imageGallery}>{getImages()}</div>
      </Row>
      <Divider orientation="center">MAP</Divider>
      <iframe className={styles.map} src={get_maps_url()}></iframe>
    </>
  );
}
