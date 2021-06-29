import { PlusOutlined } from '@ant-design/icons';
import { Button, message, Input, Drawer } from 'antd';
import React, { useState, useRef, useEffect } from 'react';
import { useIntl, FormattedMessage } from 'umi';
import { PageContainer, FooterToolbar } from '@ant-design/pro-layout';
import type { ProColumns, ActionType } from '@ant-design/pro-table';
import ProTable from '@ant-design/pro-table';
import ProForm, {
  ModalForm,
  ProFormDigit,
  ProFormText,
  ProFormTextArea,
} from '@ant-design/pro-form';
import {
  getProjects,
  addProject,
  updateProject,
  removeProject,
  removeProjects,
  updateProjects,
} from '@/services/ant-design-pro/project';
import { Form } from 'antd';

// const intl = useIntl();

const handleRemoves = async (fields: Project.ProjectItem[]) => {
  const hide = message.loading('正在添加');
  try {
    await removeProjects([...fields]);
    hide();
    message.success('添加成功');
    return true;
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

const handleUpdates = async (fields: Project.ProjectItem[]) => {
  const hide = message.loading('正在添加');
  try {
    await updateProjects([...fields]);
    hide();
    message.success('添加成功');
    return true;
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

const handleRemove = async (fields: Project.ProjectItem) => {
  const hide = message.loading('正在添加');
  try {
    await removeProject({ ...fields });
    hide();
    message.success('添加成功');
    return true;
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

/**
 * 添加节点
 *
 * @param fields
 */
const handleAdd = async (fields: Project.ProjectItem) => {
  const hide = message.loading('正在添加');
  try {
    await addProject({ ...fields });
    hide();
    message.success('添加成功');
    return true;
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

/**
 * 更新节点
 *
 * @param fields
 */
const handleUpdate = async (fields: Project.ProjectItem) => {
  const hide = message.loading('正在配置');
  try {
    await updateProject({
      ...fields,
    });
    hide();

    message.success('配置成功');
    return true;
  } catch (error) {
    hide();
    message.error('配置失败请重试！');
    return false;
  }
};

const ProjectList: React.FC = () => {
  const [createModalVisible, handleModalVisible] = useState<boolean>(false);
  const [updateModalVisible, handleUpdateModalVisible] = useState<boolean>(false);
  const [updatesModalVisible, handleUpdatesModalVisible] = useState<boolean>(false);
  const [removeModalVisible, handleRemoveModalVisible] = useState<boolean>(false);
  const [removesModalVisible, handleRemovesModalVisible] = useState<boolean>(false);

  const actionRef = useRef<ActionType>();

  const [selectedRowsState, setSelectedRows] = useState<Project.ProjectItem[]>([]);
  const [currentRow, setCurrentRow] = useState<Project.ProjectItem>();

  const [form] = Form.useForm();

  const columns: ProColumns<Project.ProjectItem>[] = [
    {
      title: <FormattedMessage id="pages.project.project.name" defaultMessage="项目名称" />,
      dataIndex: 'project_name',
      sorter: true,
    },
    {
      title: <FormattedMessage id="pages.project.project.description" />,
      dataIndex: 'project_desc',
      valueType: 'textarea',
      sorter: true,
    },
    {
      title: <FormattedMessage id="pages.project.project.creator" />,
      dataIndex: 'create_user',
      sorter: true,
    },
    {
      title: <FormattedMessage id="pages.project.project.create_date" />,
      dataIndex: 'create_date',
      // valueType: 'datetime',
      sorter: true,
    },
    {
      title: <FormattedMessage id="pages.project.project.status" />,
      dataIndex: 'status',
      sorter: true,
    },
    {
      title: <FormattedMessage id="pages.searchTable.titleOption" defaultMessage="操作" />,
      dataIndex: 'option',
      valueType: 'option',
      render: (_, record) => [
        <a
          key="config"
          onClick={() => {
            form.setFieldsValue({ ...record });
            setCurrentRow(record);
            handleUpdateModalVisible(true);
          }}
        >
          更新
        </a>,
        <a
          key="delete"
          onClick={() => {
            setCurrentRow(record);
            handleRemoveModalVisible(true);
          }}
        >
          删除
        </a>,
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable
        headerTitle="盘点项目"
        actionRef={actionRef}
        rowKey="id"
        search={{
          labelWidth: 120,
        }}
        toolBarRender={() => [
          <Button
            type="primary"
            key="create"
            onClick={() => {
              handleModalVisible(true);
            }}
          >
            <PlusOutlined /> 新建
          </Button>,
        ]}
        request={getProjects}
        columns={columns}
        rowSelection={{
          onChange: (_, selectedRows) => {
            setSelectedRows(selectedRows);
          },
        }}
        tableAlertRender={() => false}
        // expandable={{ expandedRowRender }}
      />
      {selectedRowsState?.length > 0 && (
        <FooterToolbar
          extra={
            <div>
              <FormattedMessage id="pages.searchTable.chosen" defaultMessage="已选择" />{' '}
              <a style={{ fontWeight: 600 }}>{selectedRowsState.length}</a>{' '}
              <FormattedMessage id="pages.searchTable.item" defaultMessage="项" />
              &nbsp;&nbsp;
            </div>
          }
        >
          <Button
            onClick={async () => {
              handleUpdatesModalVisible(true);
            }}
          >
            <FormattedMessage id="pages.searchTable.batchUpdate" defaultMessage="批量更新" />
          </Button>
          <Button
            type="dashed"
            onClick={async () => {
              handleRemovesModalVisible(true);
            }}
          >
            <FormattedMessage id="pages.searchTable.batchDeletion" defaultMessage="批量删除" />
          </Button>
        </FooterToolbar>
      )}
      <ModalForm
        title="新建项目"
        width="400px"
        visible={createModalVisible}
        onVisibleChange={handleModalVisible}
        onFinish={async (value) => {
          const success = await handleAdd(value as Project.ProjectItem);
          if (success) {
            handleModalVisible(false);
            if (actionRef.current) {
              actionRef.current.reload();
            }
          }
        }}
      >
        <ProFormText
          rules={[
            {
              required: true,
              message: '项目名称为必填项',
            },
          ]}
          width="md"
          name="project_name"
          label="项目名称"
          tooltip="最长为40位"
          placeholder="请输入项目名称"
        />
        <ProFormTextArea
          width="md"
          name="project_desc"
          label="项目描述"
          placeholder="请输入项目描述"
        />
        <ProFormText width="md" name="create_user" label="创建人" placeholder="请输入创建人" />
      </ModalForm>
      <ModalForm
        form={form}
        title="配置项目"
        width="400px"
        visible={updateModalVisible}
        onVisibleChange={handleUpdateModalVisible}
        onFinish={async (value) => {
          value.id = currentRow?.id;
          const success = await handleUpdate(value as Project.ProjectItem);
          if (success) {
            handleUpdateModalVisible(false);
            if (actionRef.current) {
              actionRef.current.reload();
            }
          }
        }}
      >
        <ProFormText
          rules={[
            {
              required: true,
              message: '项目名称为必填项',
            },
          ]}
          width="md"
          name="project_name"
          label="项目名称"
          tooltip="最长为40位"
          placeholder="请输入项目名称"
          initialValue={currentRow?.project_name}
        />
        <ProFormTextArea
          width="md"
          name="project_desc"
          label="项目描述"
          placeholder="请输入项目描述"
          initialValue={currentRow?.project_desc}
        />
        <ProFormText
          width="md"
          name="create_user"
          label="创建人"
          placeholder="请输入创建人"
          initialValue={currentRow?.create_user}
        />
        <ProFormDigit
          width="md"
          name="project_status"
          label="状态标识"
          placeholder="请输入状态标识"
          min={1}
          max={20}
          initialValue={currentRow?.status}
        />
      </ModalForm>
      <ModalForm
        title="配置多个项目"
        width="400px"
        visible={updatesModalVisible}
        onVisibleChange={handleUpdatesModalVisible}
        onFinish={async (value) => {
          const values = [value, ...selectedRowsState];
          const success = await handleUpdates(values as Project.ProjectItem[]);
          if (success) {
            handleUpdatesModalVisible(false);
            if (actionRef.current) {
              actionRef.current.reload();
            }
          }
        }}
      >
        <ProFormTextArea
          width="md"
          name="project_desc"
          label="项目描述"
          placeholder="请输入项目描述"
        />
        <ProFormText width="md" name="create_user" label="创建人" placeholder="请输入创建人" />
        <ProFormDigit
          width="md"
          name="status"
          label="状态标识"
          placeholder="请输入状态标识"
          min={1}
          max={20}
        />
      </ModalForm>
      <ModalForm
        title="是否删除该项目"
        width="400px"
        visible={removeModalVisible}
        onVisibleChange={handleRemoveModalVisible}
        onFinish={async () => {
          const success = await handleRemove(currentRow as Project.ProjectItem);
          if (success) {
            handleRemoveModalVisible(false);
            if (actionRef.current) {
              actionRef.current.reload();
            }
          }
        }}
      />
      <ModalForm
        title="是否删除所选项目"
        width="400px"
        visible={removesModalVisible}
        onVisibleChange={handleRemovesModalVisible}
        onFinish={async () => {
          const success = await handleRemoves(selectedRowsState);
          if (success) {
            handleRemovesModalVisible(false);
            setSelectedRows([]);
            actionRef.current?.reload?.();
          }
        }}
      />
    </PageContainer>
  );
};

export default ProjectList;
