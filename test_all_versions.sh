#!/bin/bash

echo "Testing all weekly versions..."
echo

for week in WEEK7 WEEK8 WEEK9 ""; do
  if [ -z "$week" ]; then
    file="ProgFunA2_s4134316.py"
    label="Week 10 (Final)"
  else
    file="ProgFunA2_s4134316_${week}.py"
    label="$week"
  fi

  echo "=== Testing $label ==="
  result=$(echo -e "2\n0" | timeout 3 python3 "$file" files_PASSlevel/customers.txt files_PASSlevel/products.txt 2>&1)

  if echo "$result" | grep -q "ID: V5, Name: Harry"; then
    echo "✓ $label works correctly"
  else
    echo "✗ $label has issues"
  fi
  echo
done

echo "All tests complete!"
