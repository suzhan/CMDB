<template>
    <el-tabs type="border-card">
        <!--概览-->
        <el-tab-pane>
            <span slot="label"><i class="el-icon-date"></i> 概览</span>
                <el-row>
                    <el-col>
                        <div style="float: right;" >
                            <el-select @change="fnBranchChange" v-model="branch_value"  placeholder="请选择分支">
                               <el-option
                                     v-for="item in branch_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select @change="fnSoftwareTypeChange" v-model="software_type_value" style="margin-left: 20px;" filterable placeholder="请选择应用类别">
                                <el-option
                                  v-for="item in software_type_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col>
                        <el-table :data="tableData" stripe medium style="width: 100%; margin-top: 20px">
                            <el-table-column type="index" width="50"></el-table-column>
                            <el-table-column prop="name" label="应用名" width="180"></el-table-column>
                            <el-table-column prop="version" label="版本" width="80"></el-table-column>
                            <el-table-column prop="port1" label="端口1" width="80"></el-table-column>
                            <el-table-column prop="port2" label="端口2" width="80"></el-table-column>
                            <el-table-column prop="git_path" label="源码地址" ></el-table-column>
                            <el-table-column label="操作" width="160">
                              <template slot-scope="scope">
                                <el-button
                                  size="mini"
                                  @click="handleEdit(scope.$index, scope.row)">状态</el-button>
                                <el-button
                                  size="mini"
                                  type="danger"
                                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                              </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
        </el-tab-pane>
        <!--编辑-->
        <el-tab-pane>
            <span slot="label"><i class="el-icon-edit"></i> 编辑</span>
            <!--查询表单-->
            <el-row>
                <!--<el-col :span="8">-->
                    <!--<div class="grid-content bg-purple-dark">-->
                        <!--<el-input placeholder="请输入应用名称进行搜索" v-model="software_search" @keyup.enter.native="software_search_submit">-->
                            <!--<i slot="prefix" class="el-input__icon el-icon-search"></i>-->
                        <!--</el-input>-->
                    <!--</div>-->
                  <!--</el-col>-->

                <el-col :span="16">
                    <el-select @change="software_search_submit" v-model="software_search"  filterable placeholder="搜索">
                                    <el-option
                                      v-for="item in software_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                    </el-option>
                    </el-select>
                </el-col>
            </el-row>
            <!--表单开始-->
            <el-form  :show-message="false"  ref="softwareForm" :model="softwareForm"  :rules="softwareRules"  label-width="280px" style="margin-top: 20px" >
                <!--行一-->
                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="名称" prop="softwareForm_name" >
                            <el-input v-model="softwareForm.softwareForm_name" ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" ></el-col>
                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="所属软件类别" prop="softwareForm_software_type" >
                            <el-select v-model="softwareForm.softwareForm_software_type"  filterable placeholder="请选择软件类别">
                                <el-option
                                  v-for="item in software_type_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddSoftwareTypeDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                <addSoftwareTypeDialog
                        :visible="addSoftwareTypeDialogVisible"
                        label="请输入软件类别名称"
                        @closeCallback="fnSoftwareTypeCloseDialog">
                        <!--@addSoftwareTypeCallback="fnAddSoftwareType">-->
                </addSoftwareTypeDialog>

                <!--行2-->
                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="版本" prop="softwareForm_version" >
                            <el-input v-model="softwareForm.softwareForm_version" ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" ></el-col>
                    <el-col :span="10">
                        <el-form-item label="源码地址" prop="softwareForm_git_path" >
                            <el-input v-model="softwareForm.softwareForm_git_path" ></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>



                <!--行3-->
                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="端口1" prop="softwareForm_port1" >
                            <el-input v-model="softwareForm.softwareForm_port1" ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" ></el-col>
                    <el-col :span="10">
                        <el-form-item label="端口2" prop="softwareForm_port2" >
                            <el-input v-model="softwareForm.softwareForm_port2" ></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <!--行4-->
                <el-row type="flex" >
                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="依赖软件 --> " prop="softwareForm_software" >
                            <el-select v-model="softwareForm.softwareForm_software" multiple  filterable placeholder="请选择依赖的软件">
                                <el-option
                                  v-for="item in software_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" ></el-col>
                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="依赖数据库 --> " prop="softwareForm_databases" >
                             <el-select v-model="softwareForm.softwareForm_databases" multiple placeholder="请选择">
                                <el-option-group
                                v-for="group in softwareForm_databases_group"
                                :key="group.label"
                                :label="group.label">
                                    <el-option
                                    v-for="item in group.databases_options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                    </el-option>
                                </el-option-group>
                             </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddDatabaseDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                <addDatabaseDialog
                        :visible="addDatabaseDialogVisible"
                        label="请输入新数据库名称"
                        @closeCallback="fnDatabaseCloseDialog">
                </addDatabaseDialog>

                <!--行5-->
                <el-row>
                    <el-col :span="10" >
                        <!--所属配置文件-->
                        <el-form-item label="依赖的配置文件 --> " prop="softwareForm_properties" >
                            <el-select v-model="softwareForm.softwareForm_properties" multiple filterable placeholder="请选择依赖的配置文件">
                                <el-option
                                  v-for="item in properties_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddPropertiesDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                <addPropertiesDialog
                        :visible="addPropertiesDialogVisible"
                        label="请输入新配置文件"
                        @closeCallback="fnPropertiesCloseDialog">
                </addPropertiesDialog>


                <!--行6-->
                <el-row type="flex" >
                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="所属分支 --> " prop="softwareForm_branch" >
                            <el-select v-model="softwareForm.softwareForm_branch" multiple filterable placeholder="请选择所属分支">
                                <el-option
                                  v-for="item in branch_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddBranchDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                    <addBranchDialog
                        :visible="addBranchDialogVisible"
                        label="请输入新分支"
                        @closeCallback="fnBranchCloseDialog">
                    </addBranchDialog>
                    <el-col :span="10" >
                        <!--所属主机类别-->
                        <el-form-item label="部署的节点 --> " prop="softwareForm_node" >
                            <el-select v-model="softwareForm.softwareForm_node" multiple filterable placeholder="请选择部署的节点">
                                <el-option
                                  v-for="item in node_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>


                <!--按钮-->
                <el-row type="flex" >
                    <el-col :span="24">
                        <el-form-item style="margin-left: 280px;margin-top: 20px">
                            <el-button type="primary" @click="submitForm('softwareForm')">立即创建</el-button>
                            <el-button @click="resetForm('softwareForm')">重置</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>

            </el-form>
        </el-tab-pane>
    </el-tabs>
</template>

<script>

    import addSoftwareTypeDialog from '@/components/addSoftwareTypeDialog';
    import addBranchDialog from '@/components/addBranchDialog';
    import addDatabaseDialog from  '@/components/addDatabaseDialog';
    import addPropertiesDialog from  '@/components/addPropertiesDialog';

    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "software",
        data() {
            return {
                addSoftwareTypeDialogVisible: false,
                addBranchDialogVisible: false,
                addDatabaseDialogVisible: false,
                addPropertiesDialogVisible: false,
                softwareForm: null,
                branch_value: null,
                software_type_value: null,
                branch_options: [],
                software_type_options: [],
                node_options: [],
                software_options: [],
                databases_options: [],
                properties_options: [],
                databases_mongodb_options: [],
                databases_mysql_options: [],
                softwareForm_databases_group: [],

                tableData: [],
                software_search: null,
                softwareForm: {
                    softwareForm_name: null,
                    softwareForm_software_type: null,
                    softwareForm_version: null,
                    softwareForm_port1: null,
                    softwareForm_port2: null,
                    softwareForm_git_path: null,
                    softwareForm_branch: [],
                    softwareForm_properties: [],
                    softwareForm_databases: [],
                    softwareForm_software: [],
                    softwareForm_node: []
                },
                softwareForm_node_type: [],
                softwareRules:{
                    softwareForm_name: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_software_type: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_version: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_port1: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_port2: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_git_path: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_branch: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_properties: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_databases: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_software: [
                        { required: true, message: '', trigger: 'change' }
                    ],
                    softwareForm_node:[
                        { required: true, message: '', trigger: 'change' }
                    ]
                }

            }
        },
        methods: {
            fnBranchChange() {
                console.log(this.branch_value);

                axios.post('/api/software', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.tableData = response.data.software
                })
            },
            fnSoftwareTypeChange() {
                console.log(this.software_type_value);

                axios.post('/api/software', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.tableData = response.data.software
                })
            },
            fnGetRequest() {
                axios.get('/api/software')
                .then(response => {
                    console.log(response);
                    this.branch_options = response.data.branch_options;
                    this.software_type_options = response.data.software_type_options;
                    this.node_options = response.data.node_options;
                    this.software_options = response.data.software_options;
                    this.databases_options = response.data.databases_options;
                    this.properties_options = response.data.properties_options;
                    this.softwareForm_databases_group = [{label: 'MySQL',databases_options: response.data.databases_mysql_options }, {label: 'MongoDB',databases_options: response.data.databases_mongodb_options}]

                });
            },
            software_search_submit() {
                axios.post('/api/software', {
                    software_search: this.software_search
                }).then(response => {
                    console.log(response.data.software_branch);
                    this.softwareForm.softwareForm_name = response.data.software_search[0].name;
                    this.softwareForm.softwareForm_version = response.data.software_search[0].version;
                    this.softwareForm.softwareForm_git_path = response.data.software_search[0].git_path;
                    this.softwareForm.softwareForm_port1 = response.data.software_search[0].port1;
                    this.softwareForm.softwareForm_port2 = response.data.software_search[0].port2;
                    // 软件类别
                    this.softwareForm.softwareForm_software_type = response.data.software_type[0];
                    this.softwareForm.softwareForm_branch = response.data.software_branch;
                    this.softwareForm.softwareForm_node = response.data.software_node;
                    this.softwareForm.softwareForm_software = response.data.software_software;
                    this.softwareForm.softwareForm_databases = response.data.software_databases;
                    this.softwareForm.softwareForm_properties = response.data.software_properties;
                })
            },
            submitForm: function (softwareForm) {
                this.$refs[softwareForm].validate((valid) => {
                    if (valid) {
                        axios.post('/api/software', {
                            softwareForm: this.softwareForm
                        }).then(response => {
                            console.log(response);
                            // 信息弹窗口
                            this.$alert(response.data.resultMsg[0], '信息', {
                                confirmButtonText: '确定',
                                type: response.data.resultCode[0],
                            });
                        })
                    } else {
                        console.log('error submit!!');
                        this.$alert("请填写相关资料", '信息', {
                            confirmButtonText: '确定',
                            type: 'error',
                        });
                        return false;
                    }
                });
            },
            fnOpenAddSoftwareTypeDialog() {
                this.addSoftwareTypeDialogVisible = true;
            },
            fnSoftwareTypeCloseDialog(status) {
                this.addSoftwareTypeDialogVisible = status;
            },
            fnOpenAddBranchDialog() {
                this.addBranchDialogVisible = true;
            },
            fnBranchCloseDialog(status) {
                this.addBranchDialogVisible = status;
            },
            fnOpenAddDatabaseDialog() {
                this.addDatabaseDialogVisible= true;
            },
            fnDatabaseCloseDialog(status) {
                this.addDatabaseDialogVisible = status;
            },
            fnOpenAddPropertiesDialog() {
                this.addPropertiesDialogVisible =  true;
            },
            fnPropertiesCloseDialog(status) {
                this.addPropertiesDialogVisible = status;
            },
            resetForm(softwareForm) {
                this.$refs[softwareForm].resetFields();
                this.software_search = '';
            }
        },
        mounted() {
            this.fnGetRequest()
        },
        components: {
            addSoftwareTypeDialog,
            addBranchDialog,
            addDatabaseDialog,
            addPropertiesDialog
        }
    }

</script>

<style lang="scss" scoped>
    .el-form-item {width: 95%;}
</style>