import axios from "axios"
import { useState, useEffect } from "react"
import { Company, Job, Tag } from "../utils/interfaces"
import { JobListing } from "../components/JobListing"
import { Filter } from "../components/Filter"
import { Statistics } from "../components/Statistics"

export const MainPage = () => {
  const [tags, setTags] = useState<Array<Tag>>([])
  const [jobs, setJobs] = useState<Array<Job>>([])
  const [companies, setCompanies] = useState<Array<Company>>([])
  const [filteredJobs, setFilteredJobs] = useState<Array<Job>>([])

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('http://localhost:5000/tags/all')
  
        setTags(response.data)
      } catch (error) {
        console.log('Error occured while fetching tags:', error)
      }
    }

    fetchTags()
  }, [])

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get('http://localhost:5000/jobs/all')
        const jobs = response.data
  
        setJobs(jobs)
        setFilteredJobs(jobs)
      } catch (error) {
        console.log('Error occured while fetching jobs:', error)
      }
    }

    fetchJobs()
  }, [])

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await axios.get('http://localhost:5000/company/all')
        const companies = response.data

        setCompanies(companies)
      } catch (error) {
        console.log('Error occured while fetching companies:', error)
      }
    }

    fetchCompanies()
  }, [])

  const filter = (tags: Array<string>, company: string) => {
    setFilteredJobs(
      jobs.filter(job => {
        let flag = true

        for (const each of tags) {
          if (!job.skills.includes(each)) {
            flag = false
          }
        }

        return company == "" ? flag : job.company == company && flag
      })
    )
  }

  return (
      <div style={{
        display: "flex",
        flexDirection: "column",
        gap: "35px"
      }}>
        <Filter companies={companies.map(each => each.company_name)} tags={tags.map(each => each.value)} onChange={filter}/>
        <Statistics companies={companies} jobs={jobs} />
        <JobListing jobs={filteredJobs}/>
      </div>
  )
}
