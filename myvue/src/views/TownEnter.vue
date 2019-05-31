<template>
  <el-row id="TownEnter">
    <el-col :span="5">

      <el-form ref="form" :model="ruleForm">
        <el-form-item label="小镇名称">
          <el-input v-model="ruleForm.name" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="小镇地址">
          <el-cascader
            size="large"
            :options="options"
            v-model="selectedOptions"
            @change="handleChange"
          >
          </el-cascader>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleForm)">立即创建</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <el-col :span="15">
      <el-card class="box-card" style="width: 100%">
        <el-table
          :data="tableData"
          style="width: 100%"
        >
          <el-table-column
            fixed
            prop="uid"
            label="小镇编号"
          >
          </el-table-column>
          <el-table-column
            prop="name"
            label="小镇名称"
          >
          </el-table-column>
          <el-table-column
            prop="province"
            label="省份"
          >
          </el-table-column>
          <el-table-column
            prop="city"
            label="市区"
          >
          </el-table-column>
          <el-table-column
            prop="area"
            label="区/县"
          >
          </el-table-column>

          <el-table-column
            fixed="right"
            label="操作"
            width="150">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="town_delete(scope.$index ,scope.row)"
                type="text"
                size="small">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { regionDataPlus, CodeToText } from 'element-china-area-data'
import http from '@/utils/http'
import api from '@/utils/api'
export default {
  name: 'TownEnter',
  data () {
    return {
      options: regionDataPlus,
      selectedOptions: [],
      ceshi: '',
      ruleForm: {
        name: '',
        address: {
          province: '',
          city: '',
          area: ''
        }
      },
      tableData: [

      ]
    }
  },
  methods: {
    handleChange (value) {
      this.ruleForm.address.province = CodeToText[value[0]]
      this.ruleForm.address.city = CodeToText[value[1]]
      this.ruleForm.address.area = CodeToText[value[2]]
    },
    submitForm: async function () {
      let params = this.ruleForm
      const res = await http.post(api.town_add, params)
      if (res.data) {
        console.log(res.data)
        var y = this.tableData
        y.push(res.data)
      }
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    town_message: async function () {
      let params = []
      const res = await http.post(api.town_message, params)
      if (res.data) {
        this.tableData = res.data
      }
    },
    town_delete: async function (index, row) {
      var date = { uid: row.uid }
      let params = date
      const res = await http.post(api.town_delete, params)
      if (res.data) {
        let data = res.data
        if (data.value == 1) {
          this.tableData.splice(index, 1)
        } else {
          this.$message({
            message: data.message,
            type: 'warning'
          })
        }
      }
    }
  },
  created () {
    this.town_message()
  }
}
</script>

<style>
  .el-cascader{
    margin-left: 0;
    width: 260px;
  }
</style>
