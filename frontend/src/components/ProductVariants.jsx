import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { X, Plus } from 'lucide-react';

const ProductVariants = ({ formData, setFormData }) => {
  const [newVariantName, setNewVariantName] = useState('');
  const [newVariantValue, setNewVariantValue] = useState('');

  const addVariantType = () => {
    if (!newVariantName.trim()) return;
    
    const newVariants = [
      ...formData.variants,
      { name: newVariantName, values: [] }
    ];
    
    setFormData({ ...formData, variants: newVariants, has_variants: true });
    setNewVariantName('');
  };

  const removeVariantType = (index) => {
    const newVariants = formData.variants.filter((_, i) => i !== index);
    setFormData({ 
      ...formData, 
      variants: newVariants,
      has_variants: newVariants.length > 0
    });
  };

  const addVariantValue = (variantIndex) => {
    if (!newVariantValue.trim()) return;
    
    const newVariants = [...formData.variants];
    newVariants[variantIndex].values.push(newVariantValue);
    
    setFormData({ ...formData, variants: newVariants });
    setNewVariantValue('');
  };

  const removeVariantValue = (variantIndex, valueIndex) => {
    const newVariants = [...formData.variants];
    newVariants[variantIndex].values = newVariants[variantIndex].values.filter((_, i) => i !== valueIndex);
    
    setFormData({ ...formData, variants: newVariants });
  };

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>Product Variants (Optional)</CardTitle>
        <p className="text-sm text-gray-600">Add variations like sizes, colors, materials, etc.</p>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Add Variant Type */}
        <div>
          <Label>Add Variant Type (e.g., Size, Color)</Label>
          <div className="flex gap-2 mt-2">
            <Input
              value={newVariantName}
              onChange={(e) => setNewVariantName(e.target.value)}
              placeholder="e.g., Size, Color, Material"
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addVariantType())}
            />
            <Button type="button" onClick={addVariantType} className="bg-blue-600">
              <Plus className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Display Variant Types and Values */}
        {formData.variants.map((variant, variantIndex) => (
          <Card key={variantIndex} className="bg-gray-50">
            <CardContent className="p-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-semibold text-lg">{variant.name}</h4>
                <Button
                  type="button"
                  onClick={() => removeVariantType(variantIndex)}
                  variant="ghost"
                  size="sm"
                  className="text-red-600"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              {/* Add Values */}
              <div className="mb-3">
                <Label className="text-sm">Add {variant.name} Options</Label>
                <div className="flex gap-2 mt-2">
                  <Input
                    value={newVariantValue}
                    onChange={(e) => setNewVariantValue(e.target.value)}
                    placeholder={`e.g., ${variant.name === 'Size' ? 'S, M, L' : variant.name === 'Color' ? 'Black, White' : 'Option 1'}`}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        addVariantValue(variantIndex);
                      }
                    }}
                  />
                  <Button
                    type="button"
                    onClick={() => addVariantValue(variantIndex)}
                    size="sm"
                    className="bg-green-600"
                  >
                    Add
                  </Button>
                </div>
              </div>

              {/* Display Values */}
              <div className="flex flex-wrap gap-2">
                {variant.values.map((value, valueIndex) => (
                  <div
                    key={valueIndex}
                    className="flex items-center gap-2 bg-white px-3 py-1 rounded-full border"
                  >
                    <span className="text-sm">{value}</span>
                    <button
                      type="button"
                      onClick={() => removeVariantValue(variantIndex, valueIndex)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}

        {formData.variants.length === 0 && (
          <p className="text-sm text-gray-500 text-center py-4">
            No variants added yet. Add variant types like Size or Color above.
          </p>
        )}
      </CardContent>
    </Card>
  );
};

export default ProductVariants;
