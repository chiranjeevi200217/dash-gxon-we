import os
import re

SRC_DIR = r"C:\Users\chiranjeevi\Downloads\themeforest-dtLaLdzw-gxon-hr-management-admin-dashboard-template (1)\GXON-v1.5.0-13_February_2026\xhtml\xhtml\src"
DEST_DIR = r"c:\Users\chiranjeevi\Desktop\G2\app"

# Directories we want to process (skip assets, node_modules, etc.)
VALID_DIRS = {
    "", "authentication", "chart", "components", "ecommerce", "email",
    "extended-ui", "file-manager", "forms", "icons", "invoices", "maps", "pages", "table"
}

def convert_style(match):
    style_str = match.group(1)
    declarations = []
    for item in style_str.split(';'):
        if not item.strip():
            continue
        parts = item.split(':', 1)
        if len(parts) != 2:
            continue
        k, v = parts[0].strip(), parts[1].strip()
        v_escaped = v.replace("'", "\\'")
        
        if k.startswith('--'):
            declarations.append(f"'{k}': '{v_escaped}'")
        else:
            camel_k = re.sub(r'-([a-z])', lambda m: m.group(1).upper(), k)
            declarations.append(f"{camel_k}: '{v_escaped}'")
            
    return "style={{" + ", ".join(declarations) + "}}"

def normalize_link(current_rel_dir, href):
    if not href or href.startswith('http') or href.startswith('javascript') or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
        return href, False
    
    # Strip queries and hashes
    parts = href.split('#', 1)
    base_href = parts[0]
    hash_suffix = '#' + parts[1] if len(parts) > 1 else ''
    
    q_parts = base_href.split('?', 1)
    base_href = q_parts[0]
    query_suffix = '?' + q_parts[1] if len(q_parts) > 1 else ''
    
    if not base_href:
        return hash_suffix, False
        
    # Join and normalize paths
    joined = os.path.normpath(os.path.join(current_rel_dir, base_href)).replace('\\', '/')
    if joined.startswith('../'):
        joined = joined[3:]
        
    if joined == 'index.html' or joined == 'index':
        resolved = '/'
    elif joined == 'index-rtl.html' or joined == 'index-rtl':
        resolved = '/index-rtl'
    else:
        if joined.endswith('.html'):
            resolved = '/' + joined[:-5]
        else:
            resolved = '/' + joined
            
    return resolved + query_suffix + hash_suffix, True

def convert_links(content, current_rel_dir):
    def replace_a(match):
        attrs = match.group(1)
        inner = match.group(2)
        
        href_match = re.search(r'href="([^"]*?)"', attrs)
        if not href_match:
            return match.group(0)
            
        href = href_match.group(1)
        new_href, is_internal = normalize_link(current_rel_dir, href)
        
        if is_internal:
            # Replace href in attributes
            # We escape double quotes inside href
            new_attrs = attrs.replace(f'href="{href}"', f'href="{new_href}"')
            return f'<Link{new_attrs}>{inner}</Link>'
        else:
            return match.group(0)
            
    # Non-greedily replace all standard anchor tags
    return re.sub(r'<a\b([^>]*?)>(.*?)</a>', replace_a, content, flags=re.DOTALL)

def clean_html_skeleton(html, filename):
    # Extract Title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else 'GXON HR Management Dashboard'
    
    # Remove HTML headers/footers and boilerplate
    # 1. Strip head and wrapper tags
    content = html
    head_match = re.search(r'<head>.*?</head>', content, re.DOTALL | re.IGNORECASE)
    if head_match:
        content = content.replace(head_match.group(0), '')
        
    # 2. Remove layout components that are handled globally
    # Remove header
    content = re.sub(r'<!-- begin::GXON Page Header -->.*?<!-- end::GXON Page Header -->', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove search modal
    content = re.sub(r'<div class="modal fade" id="searchResultsModal".*?(?=<!-- begin::GXON Sidebar Menu -->)', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove left sidebar
    content = re.sub(r'<!-- begin::GXON Sidebar Menu -->.*?<!-- end::GXON Sidebar Menu -->', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove right sidebar
    content = re.sub(r'<!-- begin::GXON Sidebar right -->.*?<!-- end::GXON Sidebar right -->', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove footer
    content = re.sub(r'<!-- begin::GXON Footer -->.*?<!-- end::GXON Footer -->', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Remove scripts
    content = re.sub(r'<!-- begin::GXON Page Scripts -->.*?<!-- end::GXON Page Scripts -->', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script\b[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove outer document tags
    content = re.sub(r'<!DOCTYPE html>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<html\b[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</html>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<body\b[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</body>', '', content, flags=re.IGNORECASE)
    
    # Remove <div class="page-layout"> wrappers but keep their inner content
    # A simple way is to replace the starting tag and the ending tags
    content = re.sub(r'<div class="page-layout">', '', content, flags=re.IGNORECASE)
    
    # Clean up empty lines and whitespace
    content = content.strip()
    
    # If the page wraps everything in one last </div> (matching the page-layout), strip the last </div>
    # Let's count if there is an extra closing div at the very end
    if content.endswith('</div>'):
        # Usually page-layout wraps everything. We can strip the last </div>
        content = content[:-6].strip()
        
    return title, content

def convert_to_jsx(content, current_rel_dir):
    # 1. Remove all HTML comments to avoid JSX parsing syntax errors
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # 2. Convert class -> className
    content = re.sub(r'\bclass=', 'className=', content)
    
    # 3. Convert for -> htmlFor
    content = re.sub(r'\bfor=', 'htmlFor=', content)
    
    # 4. Convert style attributes
    content = re.sub(r'style="([^"]*?)"', convert_style, content)
    
    # 5. Convert SVG attributes to camelCase
    svg_replacements = {
        r'\bstroke-width=': 'strokeWidth=',
        r'\bstroke-linecap=': 'strokeLinecap=',
        r'\bstroke-linejoin=': 'strokeLinejoin=',
        r'\bfill-rule=': 'fillRule=',
        r'\bclip-rule=': 'clipRule=',
        r'\bstroke-miterlimit=': 'strokeMiterlimit=',
        r'\bstroke-dasharray=': 'strokeDasharray=',
        r'\bstroke-dashoffset=': 'strokeDashoffset=',
        r'\bxml:space=': 'xmlSpace=',
        r'\bfont-weight=': 'fontWeight=',
        r'\bfont-size=': 'fontSize=',
        r'\bstop-color=': 'stopColor=',
        r'\bstop-opacity=': 'stopOpacity=',
        r'\bflood-opacity=': 'floodOpacity=',
        r'\bflood-color=': 'floodColor=',
    }
    for k, v in svg_replacements.items():
        content = re.sub(k, v, content)
        
    # 6. Convert self-closing tags
    content = re.sub(r'<img([^>]*?)(?<!/)>', r'<img\1 />', content)
    content = re.sub(r'<input([^>]*?)(?<!/)>', r'<input\1 />', content)
    content = re.sub(r'<br([^>]*?)(?<!/)>', r'<br\1 />', content)
    content = re.sub(r'<hr([^>]*?)(?<!/)>', r'<hr\1 />', content)
    
    # 7. Convert absolute assets references
    content = re.sub(r'src="(?:\.\./)*assets/', 'src="/assets/', content)
    content = re.sub(r'href="(?:\.\./)*assets/', 'href="/assets/', content)
    
    # 8. Convert links to Link component
    content = convert_links(content, current_rel_dir)
    
    # 9. Handle JS braces inside HTML (like page title, text blocks)
    # Escape any bare { and } that are not style props
    # We can replace { with {"{"} and } with {"}"} but let's do it safely
    # If a { is followed by { it is a style prop. Otherwise we escape it.
    # To keep it simple and robust, let's replace bare '{' and '}'
    # But only if they are not part of style={{ ... }}
    # A simple regex replacement:
    # content = content.replace('{', '{"{"}').replace('}', '{"}"}')
    # Wait, we have style={{ ... }} in our code now! So we cannot just replace all { and }.
    # Let's write a safe replacer:
    # Temporarily hide style={{...}}
    style_blocks = []
    def hide_style(m):
        style_blocks.append(m.group(0))
        return f"__STYLE_BLOCK_{len(style_blocks)-1}__"
    
    content = re.sub(r'style=\{\{[^}]*?\}\}', hide_style, content)
    
    # Also hide <Link ...> tags temporarily to avoid escaping braces inside attributes
    link_tags = []
    def hide_link(m):
        link_tags.append(m.group(0))
        return f"__LINK_TAG_{len(link_tags)-1}__"
    
    content = re.sub(r'<Link\b[^>]*?>', hide_link, content)
    content = re.sub(r'</Link>', lambda m: hide_link(m), content)
    
    # Escape braces in the remaining content
    content = content.replace('{', '{"{"}').replace('}', '{"}"}')
    
    # Replace back the links and styles
    for i, block in enumerate(style_blocks):
        content = content.replace(f"__STYLE_BLOCK_{i}__", block)
    for i, tag in enumerate(link_tags):
        content = content.replace(f"__LINK_TAG_{i}__", tag)
        
    # Replace HTML entities and unescaped >
    content = content.replace('&nbsp;', '\u00a0')
    content = content.replace('&times;', '\u00d7')
    content = content.replace('&bull;', '\u2022')
    # Replace standalone > to &gt; (hacky but works for text nodes not breaking HTML tags if we assume spaces around it)
    content = content.replace(' > ', ' &gt; ')
    
    return content

def main():
    print("Starting HTML to Next.js conversion...")
    count = 0
    
    for root, dirs, files in os.walk(SRC_DIR):
        # Calculate relative path from SRC_DIR
        rel_path = os.path.relpath(root, SRC_DIR)
        if rel_path == '.':
            rel_path = ''
            
        # Standardize separator
        rel_path = rel_path.replace('\\', '/')
        
        # Check if this directory should be processed
        dir_first_part = rel_path.split('/')[0] if rel_path else ''
        if dir_first_part not in VALID_DIRS:
            continue
            
        for file in files:
            if not file.endswith('.html'):
                continue
                
            # Exclude asset HTML files (like index.html in lucide folder)
            if 'assets' in rel_path.split('/'):
                continue
                
            src_file_path = os.path.join(root, file)
            print(f"Processing: {src_file_path}")
            
            with open(src_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            title, cleaned_body = clean_html_skeleton(html_content, file)
            jsx_content = convert_to_jsx(cleaned_body, rel_path)
            
            # Determine destination folder name
            file_base = file[:-5] # strip .html
            
            if file_base == 'index' and rel_path == '':
                # Root index
                dest_page_dir = DEST_DIR
            elif file_base == 'index' and rel_path != '':
                # Subdirectory index (e.g. ecommerce/index.html) -> app/ecommerce
                dest_page_dir = os.path.join(DEST_DIR, rel_path)
            else:
                # E.g. Leave.html -> app/leave
                # ecommerce/products.html -> app/ecommerce/products
                dest_page_dir = os.path.join(DEST_DIR, rel_path, file_base)
                
            os.makedirs(dest_page_dir, exist_ok=True)
            dest_file_path = os.path.join(dest_page_dir, 'page.js')
            
            # Format component name
            comp_name_base = file_base.replace('-', ' ').replace('_', ' ').title().replace(' ', '')
            if rel_path:
                rel_title = rel_path.replace('/', ' ').title().replace(' ', '')
                comp_name = f"{rel_title}{comp_name_base}Page"
            else:
                comp_name = f"{comp_name_base}Page"
                
            # Make sure component name is a valid JS identifier
            comp_name = re.sub(r'[^a-zA-Z0-9]', '', comp_name)
            if not comp_name[0].isalpha():
                comp_name = "Page" + comp_name
                
            # React page code template
            page_code = f"""import Link from 'next/link';

export const metadata = {{
  title: '{title}',
}};

export default function {comp_name}() {{
  return (
    <>
      {jsx_content}
    </>
  );
}}
"""
            with open(dest_file_path, 'w', encoding='utf-8') as f:
                f.write(page_code)
                
            count += 1
            
    print(f"Completed! Converted {count} pages successfully.")

if __name__ == '__main__':
    main()
