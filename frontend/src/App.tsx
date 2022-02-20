import { Layout, Menu } from 'antd';
import { MailOutlined } from '@ant-design/icons';
import { Routes, Route, useNavigate } from 'react-router-dom';
import PropertiesTab from './tabs/Properties';
import LoadConfigTab from './tabs/LoadConfig';
import AddLoadConfigTab from './tabs/AddLoadConfig';
import DataLoadsTab from './tabs/DataLoads';
const { Header, Content, Footer } = Layout;

export default function App() {
  const navigate = useNavigate();

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
            <Route path="/" element={<PropertiesTab />} />
            <Route path="/properties" element={<PropertiesTab />} />
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
