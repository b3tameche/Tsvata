import { useState } from 'react'
import { CompanyFilter } from './CompanyFilter';
import { TagFilter } from './TagFilter';
import styled from 'styled-components';

const FilterWrapper = styled.div`
  display: flex;
  justify-content: center;
  padding-top: 50px;

  .tag-filter {
    margin-right: 7px;
  }

  .company-filter {
    margin-left: 7px;
    margin-right: 7px;
  }

  button {
    margin-left: 7px;
    border: none;
    border-radius: 5px;
    padding: 0 10px 0 10px;
    background-color: #faf7f5;
    border: 1px solid #323437;
  }

  button:hover {
    background-color: #fcdefc;
    cursor: pointer;
  }
`

interface Props {
  tags: Array<string>
  companies: Array<string>
  onChange: Function
}

export const Filter = (props: Props) => {

  const [tags, setTags] = useState<Array<string>>([])
  const [company, setCompany] = useState<string>("")

  return (
    <FilterWrapper>
      <div className='tag-filter'>
        <TagFilter tags={props.tags} onChange={setTags} />
      </div>
      <div className='company-filter'>
        <CompanyFilter companies={props.companies} onChange={setCompany} />
      </div>
      <button onClick={() => props.onChange(tags, company)} style={{fontFamily: "Iosevka Curly", height: "34px"}}>Search</button>
    </FilterWrapper>
  )
}
