import { Button } from 'antd';
import React from 'react';
import './App.less';
import { getXeResult } from './requests/axios';

export default function App() {
  const getResult = () => {
    const response = getXeResult();
    console.log(response);
  };

  return (
    <div className="App">
      <Button onClick={() => getResult()}>GET RESULTS</Button>
    </div>
  );
}
