<template>
 <el-tabs type="border-card">
         <el-tab-pane>
             <span slot="label"><i class="el-icon-date"></i> 概览</span>
                <el-row>
                    <el-col>
                        <div style="float: right;" >
                            <el-select @change="fnPersonTypeChange" v-model="person_type_value" filterable placeholder="请选择人员分类">
                               <el-option
                                     v-for="item in person_type_options"
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
                            <el-table-column type="index" width="30"></el-table-column>
                            <el-table-column prop="name" label="姓名"></el-table-column>
                            <el-table-column prop="phone" label="电话"></el-table-column>
                            <el-table-column prop="email" label="电子邮件"></el-table-column>
                            <el-table-column label="操作">
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
         <el-tab-pane>
             <span slot="label"><i class="el-icon-date"></i> 编辑</span>
             <!--查询表单-->
             <el-row>
                 <el-col :span="8">
                     <div class="grid-content bg-purple-dark">
                         <el-input placeholder="请输入姓名进行搜索" v-model="person_search" @keyup.enter.native="person_search_submit">
                             <i slot="prefix" class="el-input__icon el-icon-search"></i>
                         </el-input>
                     </div>
                 </el-col>
             </el-row>
             <el-form  :show-message="false"  ref="personForm" :model="personForm"  :rules="personRules"  label-width="280px" style="margin-top: 20px" >
                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="姓名" prop="personForm_name" >
                            <el-input v-model="personForm.personForm_name" ></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" >
                       <!--所属于人员类别-->
                        <el-form-item label="所属人员类别 -->"  prop="personForm_person_type" >
                            <el-select v-model="personForm.personForm_person_type" value-key="value"  filterable placeholder="请选择所属人员类别">
                                <el-option
                                     v-for="item in person_type_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="1" >
                        <div><el-button type="text" @click="fnOpenAddPersonTypeDialog"><i class="el-icon-plus"></i></el-button></div>
                    </el-col>
                </el-row>
                 <!--调用components共用资源-->
                <addPersonTypeDialog
                        :visible="addPersonTypeDialogVisible"
                        label="请输入新人员类别"
                        @closeCallback="fnPersonTypeCloseDialog">
                </addPersonTypeDialog>




                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="电话" prop="personForm_phone">
                            <el-input v-model="personForm.personForm_phone"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10" >
                       <!--所属于分支-->
                        <el-form-item label="所属分支 -->"  prop="personForm_branch">
                            <el-select v-model="personForm.personForm_branch" value-key="value" multiple filterable placeholder="请选择所属于分支">
                                <el-option
                                     v-for="item in branch_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row type="flex" >
                    <el-col :span="10">
                        <el-form-item label="EMail" prop="personForm_email">
                            <el-input v-model="personForm.personForm_email"></el-input>
                        </el-form-item>
                    </el-col>
                     <el-col :span="10" >
                        <!--所属于软件-->
                        <el-form-item label="所属软件 -->" prop="personForm_software" >
                            <el-select v-model="personForm.personForm_software" value-key="value" multiple filterable placeholder="请选择所属软件">
                                <el-option
                                     v-for="item in software_options"
                                      :key="item.value"
                                      :label="item.label"
                                      :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>


                <el-row type="flex" >
                    <el-col :span="24">
                        <el-form-item style="margin-left: 280px;margin-top: 20px">
                            <el-button type="primary" @click="submitForm('personForm')">立即创建</el-button>
                            <el-button @click="resetForm('personForm')">重置</el-button>
                        </el-form-item>
                    </el-col>
                </el-row>

             </el-form>
         </el-tab-pane>
    </el-tabs>
</template>

<script>

    import addPersonTypeDialog from '@/components/addPersonTypeDialog';

    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "person",
        data() {
            return {
                addPersonTypeDialogVisible: false,
                person_search: null,
                person_type_value: [],

                person_type_options: [],
                branch_options: [],
                software_options: [],

                tableData: [],
                personForm: {
                    personForm_name: null,
                    personForm_branch: null,
                    personForm_phone: null,
                    personForm_software: null,
                    personForm_email: null,
                    personForm_databases: null,
                    personForm_person_type: null
                },

                personRules: {
                    personForm_name: [
                      { required: true, message: '', trigger: 'change' }
                    ],
                    personForm_phone: [
                      { required: true, message: '', trigger: 'change' }
                    ],
                    personForm_person_type: [
                      { required: true, message: '', trigger: 'change' }
                    ],
                    personForm_email: [
                      { required: true, message: '', trigger: 'change' }
                    ]
                }
            }
        },
        methods: {
            fnPersonTypeChange() {
                axios.post('/api/person', {
                    person_type_select: this.person_type_value
                }).then(response => {
                    console.log(response);
                    this.tableData = response.data.person
                })
            },
            person_search_submit() {
                axios.post('/api/person', {
                    person_search: this.person_search,
                }).then(response => {
                    console.log(response);
                    this.personForm.personForm_name = response.data.person_result[0].name;
                    this.personForm.personForm_phone = response.data.person_result[0].phone;
                    this.personForm.personForm_email = response.data.person_result[0].email;
                    // 单选
                    this.personForm.personForm_person_type = response.data.person_type_result[0];
                    // 多选框
                    this.personForm.personForm_branch = response.data.person_branch_result;
                    this.personForm.personForm_software = response.data.person_software_result;
                })
            },
            submitForm: function (personForm) {
                this.$refs[personForm].validate((valid) => {
                    if (valid) {
                        axios.post('/api/person', {
                            personForm: this.personForm
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
            resetForm(personForm) {
                this.$refs[personForm].resetFields();
                this.person_search = '';
            },
            fnGetRequest() {
                axios.get('/api/person')
                    .then(response => {
                        console.log(response);
                        this.person_type_options = response.data.person_type_options;
                        this.branch_options = response.data.branch_options;
                        this.software_options = response.data.software_options;
                        this.databases_options = response.data.databases_options;
                });
            },
            fnOpenAddPersonTypeDialog() {
                this.addPersonTypeDialogVisible = true;
            },
            fnPersonTypeCloseDialog(status) {
                console.log('visible status', status);
                this.addPersonTypeDialogVisible = status;
            },

        },
        mounted() {
            this.fnGetRequest()
        },
        components: {
            addPersonTypeDialog
        }
    }
</script>

<style lang="scss" scoped>

</style>