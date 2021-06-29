// @ts-ignore
/* eslint-disable */

import { request } from 'umi';

export async function getProjects(
  params: {
    current?: number;
    pageSize?: number;
  },
  sorter?: { [key: string]: any },
  options?: { [key: string]: any },
) {
  return request<Project.ProjectList>('/api/inventory/getProjects/', {
    method: 'GET',
    params: {
      ...params,
      sorter,
    },
    ...(options || {}),
  });
}

export async function updateProject(body: Project.ProjectItem, options?: { [key: string]: any }) {
  return request('/api/inventory/updateProject/', {
    method: 'POST',
    data: body,
    ...(options || {}),
  });
}

export async function addProject(body: Project.ProjectItem, options?: { [key: string]: any }) {
  return request('/api/inventory/addProject/', {
    method: 'POST',
    data: body,
    ...(options || {}),
  });
}

export async function removeProject(body: Project.ProjectItem, options?: { [key: string]: any }) {
  return request('/api/inventory/removeProject/', {
    method: 'DELETE',
    data: body,
    ...(options || {}),
  });
}

export async function removeProjects(
  body: Project.ProjectItem[],
  options?: { [key: string]: any },
) {
  return request('/api/inventory/removeProjects/', {
    method: 'DELETE',
    data: body,
    ...(options || {}),
  });
}

export async function updateProjects(
  body: Project.ProjectItem[],
  options?: { [key: string]: any },
) {
  return request('/api/inventory/updateProjects/', {
    method: 'POST',
    data: body,
    ...(options || {}),
  });
}
