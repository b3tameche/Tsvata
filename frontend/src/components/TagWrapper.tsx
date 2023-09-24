import styled from 'styled-components'

const Wrapper = styled.span`
  font-size: 14px;

  & {
    color: #323437;
    border: 1px solid #323437;
    margin: 5px;
    border-radius: 5px;
    padding: 6px;
  }

  &:hover {
    background-color: #fcdefc;
    border-color: #323437;
  }
`

interface Props {
  tag: string
  style?: any
}

export const TagWrapper = (props: Props) => {
  return (
    <Wrapper style={props.style} id='job-tag'>{props.tag}</Wrapper>
  )
}
