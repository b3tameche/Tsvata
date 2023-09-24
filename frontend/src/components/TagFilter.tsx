import { useAutocomplete, AutocompleteGetTagProps } from '@mui/base/useAutocomplete';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import { styled } from '@mui/material/styles';
import { autocompleteClasses } from '@mui/material/Autocomplete';

const Root = styled('div')(
  `
    color: #323437;
    font-size: 14px;
  `,
);

const InputWrapper = styled('div')(
  `
    width: 300px;
    border: 1px solid #323437;
    background-color: #ffffff;
    border-radius: 4px;
    padding: 1px;
    display: flex;
    flex-wrap: wrap;

    &:hover {
      border-color: #acb6c2;
    }

    &.focused {
      border-color: #323437;
    }

    & input {
      background-color: white;
      color: #323437;
      height: 30px;
      box-sizing: border-box;
      padding: 4px 6px;
      width: 0;
      min-width: 30px;
      flex-grow: 1;
      border: 0;
      margin: 0;
      outline: 0;
    }
  `,
);

interface TagProps extends ReturnType<AutocompleteGetTagProps> {
  label: string;
}

function Tag(props: TagProps) {
  const { label, onDelete, ...other } = props;
  return (
    <div {...other}>
      <span>{label}</span>
      <CloseIcon onClick={onDelete} />
    </div>
  );
}

const StyledTag = styled(Tag)<TagProps>(
  `
    display: flex;
    align-items: center;
    height: 24px;
    margin: 2px;
    line-height: 22px;
    background-color: #fcdefc;
    border: 1px solid #323437;
    border-radius: 10px;
    box-sizing: content-box;
    padding: 0 4px 0 10px;
    outline: 0;
    overflow: hidden;

    &:hover {
      border-color: #acb6c2;
    }

    & span {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    & svg {
      font-size: 12px;
      cursor: pointer;
      padding: 4px;
      border: 1px;
    }
  `,
);

const Listbox = styled('ul')(
  `
    width: 300px;
    margin: 2px 0 0;
    padding: 0;
    position: absolute;
    list-style: none;
    background-color: white;
    overflow: auto;
    max-height: 250px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 1;

    & li {
      padding: 5px 12px;
      display: flex;

      & span {
        flex-grow: 1;
      }

      & svg {
        color: white;
      }
    }

    & li[aria-selected='true'] {
      background-color: #fcdefc;

      & svg {
        color: currentColor;
      }
    }

    & li.${autocompleteClasses.focused} {
      background-color: #fcdefc;
      cursor: pointer;

      & svg {
        color: currentColor;
      }
    }
  `,
);

interface Props {
  tags: Array<string>
  onChange: Function
}

export const TagFilter = (props: Props) => {
  const {
    getRootProps,
    getInputProps,
    getTagProps,
    getListboxProps,
    getOptionProps,
    groupedOptions,
    value,
    focused,
    setAnchorEl,
  } = useAutocomplete({
    id: 'tag-filter',
    multiple: true,
    options: props.tags,
    getOptionLabel: (option) => option,
    onChange: (_, value: Array<string>) => props.onChange(value)
  });

  return (
    <Root>
      <div {...getRootProps()}>
        <InputWrapper ref={setAnchorEl} className={focused ? 'focused' : ''}>
          {value.map((option: string, index: number) => (
            <StyledTag label={option} {...getTagProps({ index })} />
          ))}
          <input {...getInputProps()} placeholder="Tags..." style={{fontFamily: "Iosevka Curly"}}/>
        </InputWrapper>
      </div>
      {groupedOptions.length > 0 ? (
        <Listbox {...getListboxProps()}>
          {(groupedOptions as typeof props.tags).map((option, index) => (
            <li {...getOptionProps({option, index})}>
              <span>{option}</span>
              <CheckIcon fontSize="small" />
            </li>
          ))}
        </Listbox>
      ) : null}
    </Root>
  );
}