// utils/stringUtils.ts
export const truncateText = (
    text: string, 
    maxLength: number, 
    ellipsis: string = '...'
  ): string => {
    if (!text) return '';
    
    return text.length > maxLength 
      ? text.substring(0, maxLength).trim() + ellipsis
      : text;
  };
  
  export const capitalizeFirstLetter = (text: string): string => {
    return text ? text.charAt(0).toUpperCase() + text.slice(1) : '';
  };