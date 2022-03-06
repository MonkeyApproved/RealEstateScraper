import styles from './Tabs.module.css';
import { Button, Form, Input, InputNumber, message, Radio } from 'antd';
import { LoadConfig, postLoadConfig } from '../requests/data_manager';

export default function AddLoadConfigTab() {
  const [form] = Form.useForm();

  const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
  };

  const onSubmit = (values: Omit<LoadConfig, 'id'>) => {
    postLoadConfig(values)
      .then((response) => {
        message.info(`New config added: ${response.statusText} (${response.status})`);
      })
      .catch((error) => {
        message.error(`Failed to get load_config: ${error}`);
      });
  };

  const onReset = () => {
    form.resetFields();
  };

  return (
    <div className={styles.content}>
      <Form
        {...layout}
        form={form}
        name="control-hooks"
        onFinish={onSubmit}
        initialValues={{ frequency: 24, maximum_price: 200000 }}
      >
        <Form.Item name="config_name" label="Config name" rules={[{ required: true }]}>
          <Input placeholder="give this configuration a meaningful name" />
        </Form.Item>
        <Form.Item name="frequency" label="Frequency" rules={[{ required: true }]}>
          <Radio.Group>
            <Radio.Button value={1}>Hourly</Radio.Button>
            <Radio.Button value={24}>Daily</Radio.Button>
            <Radio.Button value={24 * 7}>Weekly</Radio.Button>
          </Radio.Group>
        </Form.Item>
        <Form.Item name="item_type" label="Type" rules={[{ required: true }]}>
          <Radio.Group>
            <Radio.Button value="re_residence">Apartment</Radio.Button>
            <Radio.Button value="re_land">Land</Radio.Button>
          </Radio.Group>
        </Form.Item>
        <Form.Item name="geo_place_id" label="Location" rules={[{ required: true }]}>
          <Radio.Group>
            <Radio.Button value="ChIJ8UNwBh-9oRQR3Y1mdkU1Nic">Athens</Radio.Button>
            <Radio.Button value="ChIJ11DRvwBcWxMREJS54iy9AAQ">Corfu</Radio.Button>
          </Radio.Group>
        </Form.Item>
        <Form.Item name="maximum_price" label="Max price">
          <InputNumber />
        </Form.Item>
        <Form.Item name="minimum_construction_year" label="Min constr. year">
          <InputNumber />
        </Form.Item>
        <Form.Item name="minimum_size" label="Min size">
          <InputNumber />
        </Form.Item>
        <Form.Item wrapperCol={{ offset: 4, span: 16 }}>
          <Button type="primary" htmlType="submit">
            Add
          </Button>
          <Button htmlType="button" onClick={onReset}>
            Reset
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
