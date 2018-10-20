<template>
    <el-tabs type="border-card">
         <el-tab-pane>
             <span slot="label"><i class="el-icon-date"></i> 概览</span>
                <el-row>
                    <el-col>
                        <div style="float: right;" >
                            <el-select @change="fnBranchChange" v-model="branch_value" filterable placeholder="请选择分支">
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
                             <el-select @change="fnSoftwareNameChange" v-model="software_name_value" style="margin-left: 20px;" filterable placeholder="请选择应用名">
                                <el-option
                                  v-for="item in software_name_options"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col v-for="(item, index) in tableData">
                       {{ index }}&nbsp;&nbsp;
                           {{ item }}
                    </el-col>
                </el-row>
         </el-tab-pane>
    </el-tabs>
</template>

<script>
    const axios = require('axios');

    var axiosDefaults = require("axios/lib/defaults");
    axiosDefaults.xsrfCookieName = "csrftoken";
    axiosDefaults.xsrfHeaderName = "X-CSRFToken";
    axiosDefaults.withCredentials = true;

    export default {
        name: "properties",
        data() {
            return {
                branch_value: null,
                software_type_value: null,
                software_name_value: null,
                branch_options: [],
                software_type_options: [],
                software_name_options: [],
                tableData: [],
                newStr: []
            }
        },
        methods: {
            fnBranchChange() {
                console.log(this.branch_value);

                axios.post('/api/properties', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.software_name_options = response.data.software_name_options;
                })
            },
            fnSoftwareTypeChange() {
                console.log(this.software_type_value);

                axios.post('/api/properties', {
                    branch_select: this.branch_value,
                    software_type_select: this.software_type_value
                }).then(response => {
                    console.log(response);
                    this.software_name_options = response.data.software_name_options;
                    // var newStr = response.data.split("\n")
                    // console.log('testtest', newStr)
                    // this.tableData = newStr
                })
            },
            fnSoftwareNameChange() {
                axios.post('/api/properties', {
                    software_name_select: this.software_name_value,
                    branch_select: this.branch_value
                }).then(response => {
                    console.log(response);
                    // this.software_name_options = response.data.software_name_options;
                    // 将信息按换行符来拆开显示
                    var newStr = response.data.split("\n");
                    this.tableData = newStr
                })
            },
            fnGetRequest() {
                axios.get('/api/node')
                .then(response => {
                    console.log(response);
                    this.branch_options = response.data.branch_options;
                    this.software_type_options = response.data.software_type_options;
                    this.software_name_options = response.data.software_name_options;
                    // this.master_options = response.data.master_options;
                    // this.business_line_options = response.data.business_line_options;
                    // this.node_type_options = response.data.node_type_options;
                });
            }
        },
        mounted() {
            this.fnGetRequest()
        },
    }

</script>

<style lang="scss" scoped>

</style>