import { Layout, Menu, message } from 'antd';
import { MailOutlined } from '@ant-design/icons';
import { Routes, Route, useNavigate } from 'react-router-dom';
import PropertiesTab from './tabs/Properties';
import LoadConfigTab from './tabs/LoadConfig';
import AddLoadConfigTab from './tabs/AddLoadConfig';
import DataLoadsTab from './tabs/DataLoads';
import DetailsTab from './tabs/Details';
import { getXeResult, XeResult } from './requests/xe_properties';
import { useEffect, useState } from 'react';
import { PropertyTableSettings } from './table/PropertiesTable';
const { Header, Content, Footer } = Layout;

export default function App() {
  const navigate = useNavigate();
  const [properties, setProperties] = useState<XeResult[]>([]);
  const [tableSettings, setTableSettings] = useState<PropertyTableSettings>({
    count: 0,
    limit: 20,
    offset: 0,
    ordering: '',
    filter: '',
  });

  useEffect(() => {
    getXeResult(tableSettings)
      .then((response) => {
        setProperties(response.data.results);
        if (response.data.count !== tableSettings.count) {
          setTableSettings({ ...tableSettings, count: response.data.count });
        }
      })
      .catch((error) => {
        message.error(`Failed to GET Xe Results: ${error}`);
      });
  }, [tableSettings]);

  return (
    <Layout className="layout">
      <Header>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['properties']}>
          <Menu.Item
            key="properties"
            icon={<MailOutlined />}
            onClick={() => navigate('/properties')}
          >
            <span>Properties</span>
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
                <PropertiesTab
                  propertyList={properties}
                  settings={tableSettings}
                  setSettings={setTableSettings}
                />
              }
            />
            <Route
              path="/properties"
              element={
                <PropertiesTab
                  propertyList={properties}
                  settings={tableSettings}
                  setSettings={setTableSettings}
                />
              }
            />
            <Route path="/config" element={<LoadConfigTab />} />
            <Route path="/add_config" element={<AddLoadConfigTab />} />
            <Route path="/loads" element={<DataLoadsTab />} />
            <Route
              path="/details/:propertyId"
              element={
                <DetailsTab
                  propertyList={properties}
                  settings={tableSettings}
                  setSettings={setTableSettings}
                />
              }
            />
          </Routes>
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>Real Estate Scarper by MonkeyApproved</Footer>
    </Layout>
  );
}
