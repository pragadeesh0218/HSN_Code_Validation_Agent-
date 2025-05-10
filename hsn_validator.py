import re
import logging

logger = logging.getLogger(__name__)

class HSNValidator:
    def __init__(self, hsn_df):
        """
        Initialize the HSN Validator with the master HSN data.
        
        Args:
            hsn_df (pandas.DataFrame): DataFrame containing HSN codes and descriptions
        """
        self.hsn_df = hsn_df
        # Convert HSN codes to strings and create a set for faster lookups
        self.hsn_df['HSNCode'] = self.hsn_df['HSNCode'].astype(str)
        self.hsn_codes_set = set(self.hsn_df['HSNCode'].values)
        
        # Create a dictionary mapping HSN codes to their descriptions
        self.hsn_descriptions = dict(zip(self.hsn_df['HSNCode'], self.hsn_df['Description']))
        
        logger.info(f"HSN Validator initialized with {len(self.hsn_codes_set)} HSN codes")
    
    def validate(self, hsn_code):
        """
        Validate an HSN code against the master data.
        
        Args:
            hsn_code (str): The HSN code to validate
            
        Returns:
            dict: A dictionary containing validation results
        """
        # Format validation
        if not self._is_valid_format(hsn_code):
            return {
                'valid': False,
                'message': 'Invalid HSN code format. Must be 2-8 digits.',
                'validation_type': 'format'
            }
        
        # Existence validation
        if hsn_code in self.hsn_codes_set:
            return {
                'valid': True,
                'message': 'Valid HSN code found in master data.',
                'description': self.hsn_descriptions.get(hsn_code, 'No description available'),
                'validation_type': 'exact_match'
            }
        
        # Hierarchical validation
        parent_code = self._find_parent_code(hsn_code)
        if parent_code:
            return {
                'valid': True,
                'message': f'HSN code is valid as a child of parent code {parent_code}.',
                'description': self.hsn_descriptions.get(parent_code, 'No description available'),
                'parent_code': parent_code,
                'validation_type': 'hierarchical'
            }
        
        return {
            'valid': False,
            'message': 'HSN code not found in master data.',
            'validation_type': 'not_found'
        }
    
    def _is_valid_format(self, hsn_code):
        """
        Check if the HSN code has a valid format.
        
        Args:
            hsn_code (str): The HSN code to validate
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        # HSN codes should be 2-8 digits
        return bool(re.match(r'^\d{2,8}$', hsn_code))
    
    def _find_parent_code(self, hsn_code):
        """
        Find a parent code for the given HSN code.
        
        Args:
            hsn_code (str): The HSN code to find a parent for
            
        Returns:
            str or None: The parent code if found, None otherwise
        """
        # Check for parent codes by progressively removing digits from the end
        code_len = len(hsn_code)
        for i in range(code_len - 1, 1, -1):  # Start from length-1 down to 2
            parent = hsn_code[:i]
            if parent in self.hsn_codes_set:
                return parent
        
        return None
    
    def get_description(self, hsn_code):
        """
        Get the description for an HSN code.
        
        Args:
            hsn_code (str): The HSN code to look up
            
        Returns:
            str: The description if found, None otherwise
        """
        return self.hsn_descriptions.get(hsn_code)
