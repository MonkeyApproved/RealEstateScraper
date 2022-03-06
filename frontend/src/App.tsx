import { Layout, Menu, message } from 'antd';
import { AppstoreOutlined, HomeOutlined } from '@ant-design/icons';
import { Routes, Route, useNavigate } from 'react-router-dom';
import LoadConfigTab from './pages/LoadConfig';
import AddLoadConfigTab from './pages/AddLoadConfig';
import DataLoadsTab from './pages/DataLoads';
import styles from './pages/Tabs.module.css';
import { getXeResult, TableSettings, XeResult } from './requests/xe_properties';
import { useEffect, useState } from 'react';
import ApartmentTable from './table/ApartmentTable';
import LandTable from './table/LandTable';
const { Header, Content, Footer } = Layout;

export default function App() {
  const navigate = useNavigate();

  // values and settings for apartment table
  const [apartments, setApartments] = useState<XeResult[]>([]);
  const [apTableSettings, setApTableSettings] = useState<TableSettings>({
    page: 1,
    count: 0,
    limit: 20,
    offset: 0,
    ordering: '',
    filter: '&type=re_residence',
  });

  useEffect(() => {
    getXeResult(apTableSettings)
      .then((response) => {
        setApartments(response.data.results);
        if (response.data.count !== apTableSettings.count) {
          setApTableSettings({ ...apTableSettings, count: response.data.count });
        }
      })
      .catch((error) => {
        message.error(`Failed to GET Xe Results for Apartments: ${error}`);
      });
  }, [apTableSettings]);

  // values and settings for apartment table
  const [land, setLand] = useState<XeResult[]>([]);
  const [landTableSettings, setLandTableSettings] = useState<TableSettings>({
    page: 1,
    count: 0,
    limit: 20,
    offset: 0,
    ordering: '',
    filter: '&type=re_land',
  });

  useEffect(() => {
    getXeResult(landTableSettings)
      .then((response) => {
        setLand(response.data.results);
        if (response.data.count !== landTableSettings.count) {
          setLandTableSettings({ ...landTableSettings, count: response.data.count });
        }
      })
      .catch((error) => {
        message.error(`Failed to GET Xe Results for Land: ${error}`);
      });
  }, [landTableSettings]);

  return (
    <Layout className="layout">
      <Header>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['apartments']}>
          <Menu.Item
            key="apartments"
            icon={<HomeOutlined />}
            onClick={() => navigate('/apartments')}
          >
            <span>Apartments</span>
          </Menu.Item>
          <Menu.Item key="land" icon={<AppstoreOutlined />} onClick={() => navigate('/land')}>
            <span>Land</span>
          </Menu.Item>
          <Menu.Item key="config" onClick={() => navigate('/config')}>
            <span>Config</span>
          </Menu.Item>
          <Menu.Item key="add_config" onClick={() => navigate('/add_config')}>
            <span>Add</span>
          </Menu.Item>
          <Menu.Item key="loads" onClick={() => navigate('/loads')}>
            <span>Loads</span>
          </Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <div className="site-layout-content">
          <Routes>
            <Route
              path="/"
              element={
                <div className={styles.content}>
                  <ApartmentTable
                    propertyList={apartments}
                    settings={apTableSettings}
                    setSettings={setApTableSettings}
                  />
                </div>
              }
            />
            <Route
              path="/apartments"
              element={
                <div className={styles.content}>
                  <ApartmentTable
                    propertyList={apartments}
                    settings={apTableSettings}
                    setSettings={setApTableSettings}
                  />
                </div>
              }
            />
            <Route
              path="/land"
              element={
                <div className={styles.content}>
                  <LandTable
                    propertyList={land}
                    settings={landTableSettings}
                    setSettings={setLandTableSettings}
                  />
                </div>
              }
            />
            <Route path="/config" element={<LoadConfigTab />} />
            <Route path="/add_config" element={<AddLoadConfigTab />} />
            <Route path="/loads" element={<DataLoadsTab />} />
          </Routes>
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>Real Estate Scarper by MonkeyApproved</Footer>
    </Layout>
  );
}
